from .serializers import SupplierSerializer, PurchaseOrderSerializer, PurchasePriceRecordSerializer, PurchasePaymentRecordSerializer
from .models import PurchaseOrder, PurchaseGoods, PaymentRecord, PurchasePriceRecord, Supplier
from .paginations import PurchaseOrderPagination, PurchasePriceRecordPagination, PurchasePaymentRecordPagination
from utils.permissions import IsAuthenticated, PurchasePricePermission
from .permissions import SupplierPermission, PurchaseOrderPermission
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.status import HTTP_201_CREATED
from apps.warehouse.models import Inventory, Flow
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.warehouse.models import Warehouse
from django.db.models import Sum, F
from rest_framework import viewsets
from apps.account.models import Account
from django.db import transaction
from apps.goods.models import Goods
from apps.user.models import User
from utils import math
import pendulum
from .filters import PurchasePaymentRecordFilter, PurchaseOrderFilter
from .serializers import SupplierUpdateSerializer
from .paginations import SupplierPagination
from utils.excel import export_excel, import_excel
import itertools
from number_precision import NP
from apps.warehouse.models import StockInOrder, StockInGoods


class SupplierViewSet(viewsets.ModelViewSet):
    """供应商: list, create, update, destroy"""
    serializer_class = SupplierSerializer
    pagination_class = SupplierPagination
    permission_classes = [IsAuthenticated, SupplierPermission]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['number', 'name', 'address', 'remark']
    ordering_fields = ['number', 'name']
    ordering = ['number']
    field_mapping = (('number', '编号'), ('name', '名称'), ('contacts', '联系人'), ('phone', '电话'),
                     ('email', '邮箱'), ('address', '地址'), ('remark', '备注'))

    def get_serializer_class(self):
        return SupplierUpdateSerializer if self.request.method == 'PUT' else self.serializer_class

    def get_queryset(self):
        return self.request.user.teams.suppliers.all()

    def perform_create(self, serializer):
        serializer.save(teams=self.request.user.teams)

    @action(detail=False)
    def export_excel(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return export_excel(serializer.data, '供应商列表', self.field_mapping)

    @action(detail=False)
    @transaction.atomic
    def import_excel(self, request, *args, **kwargs):
        Supplier.objects.bulk_create([Supplier(**item, teams=request.user.teams)
                                      for item in import_excel(self, self.field_mapping)])
        return Response(status=HTTP_201_CREATED)


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    """采购单据: list, create, retrieve, destroy"""
    serializer_class = PurchaseOrderSerializer
    pagination_class = PurchaseOrderPagination
    permission_classes = [IsAuthenticated, PurchaseOrderPermission]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = PurchaseOrderFilter
    search_fields = ['number', 'remark']
    ordering_fields = ['number', 'date']
    ordering = ['-number']

    def get_queryset(self):
        return self.request.user.teams.purchase_orders.prefetch_related('goods_set').all()

    @transaction.atomic
    def perform_create(self, serializer):
        teams = self.request.user.teams
        order_number = self.create_purchase_number()

        # 验证外键
        supplier_id = self.request.data.get('supplier')
        supplier = Supplier.objects.filter(teams=teams, id=supplier_id).first()
        warehouse_id = self.request.data.get('warehouse')
        warehouse = Warehouse.objects.filter(teams=teams, id=warehouse_id).first()
        account_id = self.request.data.get('account')
        account = Account.objects.filter(teams=teams, id=account_id).first()
        contacts_username = self.request.data.get('contacts')
        contacts = User.objects.filter(teams=teams, username=contacts_username).first()

        if not supplier or not warehouse or not account or not contacts:
            raise APIException('供应商, 仓库, 账户, 联系人不存在')

        # 创建采购表单
        serializer.save(number=order_number, supplier_name=supplier.name, warehouse_name=warehouse.name,
                        warehouse_address=warehouse.address, account_name=account.name,
                        contacts_name=contacts.name, contacts_phone=contacts.phone, teams=teams)

        # 创建采购商品
        PurchaseGoods.objects.bulk_create(self.create_goods(serializer.instance))

    def perform_destroy(self, instance):
        if instance.is_commit:
            raise APIException('采购单据已确认提交不能删除')
        instance.delete()

    @action(detail=True)
    @transaction.atomic
    def commit(self, request, *args, **kwargs):
        order = self.get_purchase_order(kwargs.get('pk'))
        # 创建入库单据
        stock_in_order = StockInOrder.objects.create(number=self.create_stock_in_number(), warehouse=order.warehouse,
                                                     warehouse_name=order.warehouse_name, teams=request.user.teams)

        stock_in_goods_set = []
        for purchase_goods in order.goods_set.all():
            if not purchase_goods.goods:
                raise APIException(f'商品[{purchase_goods.goods_name}] 不存在')

            # 统计商品数量, 应付金额
            order.total_quantity = NP.plus(order.total_quantity, purchase_goods.quantity)
            order.total_amount = NP.plus(order.total_amount, purchase_goods.discount_amount)

            # 创建入库商品
            stock_in_goods_set.append(StockInGoods(stock_in_order=stock_in_order, goods=purchase_goods.goods,
                                                   goods_number=purchase_goods.number, goods_name=purchase_goods.name,
                                                   goods_unit=purchase_goods.unit, quantity=purchase_goods.quantity,
                                                   teams=request.user.teams))
        StockInGoods.objects.bulk_create(stock_in_goods_set)

        order.is_commit = True
        order.save()
        return Response(self.get_serializer(order).data)

    def get_purchase_order(self, pk):
        teams = self.request.user.teams
        order = PurchaseOrder.objects.prefetch_related('goods_set').filter(teams=teams, pk=pk).first()
        if not order:
            raise APIException('单据不存在')

        if order.is_commit:
            raise APIException('采购单已提交入库')

        if not order.warehouse:
            raise APIException(f'仓库[{order.warehouse_name}] 不存在')

        return order

    def create_purchase_number(self):
        return f'P{pendulum.now().format("YYYYMMDDHHmmssSSSSS")}'

    def create_stock_in_number(self):
        return f'SI{pendulum.now().format("YYYYMMDDHHmmssSSSS")}'

    def create_goods(self, purchase_order):
        teams = self.request.user.teams
        goods_set = self.request.data.get('goods_set', [])
        goods_ids = map(lambda item: item['id'], goods_set)
        goods_list = Goods.objects.filter(id__in=goods_ids, teams=teams)

        if len(goods_set) != len(goods_list):
            raise APIException('商品不存在')

        for item in itertools.product(goods_list, goods_set):
            if item[0].id == item[1]['id']:
                purchase_price = item[1].get('purchase_price', item[0].purchase_price)
                quantity, discount = (item[1].get('quantity'), item[1].get('discount'))
                if purchase_price < 0 or quantity <= 0 or discount < 0:
                    raise APIException('商品数据异常')

                discount_price = NP.times(purchase_price, discount, 0.01)
                yield PurchaseGoods(teams=teams, purchase_order=purchase_order, goods=item[0], number=item[0].number,
                                    name=item[0].name, unit=item[0].unit, purchase_price=purchase_price,
                                    quantity=quantity, amount=NP.times(purchase_price, quantity), discount=discount,
                                    discount_price=discount_price, discount_amount=NP.times(discount_price, quantity))


# class PurchaseOrderViewSet(viewsets.ModelViewSet):
#     """list, create, update, destroy"""
#     serializer_class = PurchaseOrderSerializer
#     permission_classes = [IsAuthenticated, PurchaseOrderPermission, PurchasePricePermission]
#     pagination_class = PurchaseOrderPagination
#     filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
#     filterset_class = PurchaseOrderFilter
#     search_fields = ['id', 'supplier_name', 'warehouse_name']
#     ordering_fields = ['id', 'date', 'total_amount', 'amount']
#     ordering = ['-id']

#     def get_queryset(self):
#         return self.request.user.teams.purchase_orders.all()

#     @transaction.atomic
#     def perform_create(self, serializer):
#         order_id = f'P{pendulum.now().format("YYYYMMDDHHmmssSSSS")}'
#         teams = self.request.user.teams

#         # 验证
#         if self.request.data.get('is_return', False):  # 退货单
#             purchase_order = self.request.data.get('purchase_order')
#             purchase_order = PurchaseOrder.objects.filter(
#                 id=purchase_order, is_done=True, is_return=False, teams=teams).first()
#             if not purchase_order:
#                 raise ValidationError
#             supplier = purchase_order.supplier
#             warehouse = purchase_order.warehouse
#         else:
#             supplier = self.request.data.get('supplier')
#             supplier = Supplier.objects.filter(id=supplier, teams=teams).first()
#             warehouse = self.request.data.get('warehouse')
#             warehouse = Warehouse.objects.filter(id=warehouse, teams=teams).first()

#         account = self.request.data.get('account')
#         account = Account.objects.filter(id=account, teams=teams).first()
#         contacts = self.request.data.get('contacts')
#         contacts = User.objects.filter(username=contacts, teams=teams).first()

#         if not supplier or not warehouse or not account or not contacts:
#             raise ValidationError

#         # 创建表单商品
#         goods_set = self.request.data.get('goods_set', [])
#         goods_id_set = map(lambda item: item['id'], goods_set)
#         goods_list = Goods.objects.filter(id__in=goods_id_set, teams=teams)

#         if len(goods_set) != len(goods_list):
#             raise ValidationError

#         total_quantity = 0
#         total_amount = 0
#         purchase_goods_set = []
#         for goods1 in goods_list:
#             for goods2 in goods_set:
#                 if goods1.id == goods2['id']:
#                     amount = math.times(goods2['quantity'], goods2['purchase_price'])
#                     discount_amount = math.times(amount, goods2['discount'], 0.01)
#                     discount_price = math.times(goods2['purchase_price'], goods2['discount'], 0.01)
#                     total_quantity = math.plus(total_quantity, goods2['quantity'])
#                     total_amount = math.plus(total_amount, discount_amount)

#                     purchase_goods_set.append(PurchaseGoods(goods=goods1, number=goods1.number, name=goods1.name,
#                                                             unit=goods1.unit,
#                                                             quantity=goods2['quantity'], purchase_price=goods2['purchase_price'],
#                                                             discount=goods2['discount'], discount_price=discount_price,
#                                                             amount=amount, discount_amount=discount_amount,
#                                                             purchase_order_id=order_id))
#                     break

#         serializer.save(id=order_id, supplier_name=supplier.name, warehouse_name=warehouse.name,
#                         warehouse_address=warehouse.address, account_name=account.name,
#                         contacts_name=contacts.name, contacts_phone=contacts.phone,
#                         total_quantity=total_quantity, total_amount=total_amount, teams=teams)

#         PurchaseGoods.objects.bulk_create(purchase_goods_set)

#         # 创建付款记录
#         amount = self.request.data.get('amount', 0)
#         if amount != 0:
#             PaymentRecord.objects.create(amount=amount, account=account, account_name=account.name,
#                                          purchase_order=serializer.instance)

#     def perform_destroy(self, instance):
#         if instance.is_done:
#             raise APIException
#         instance.delete()

#     @action(detail=False)
#     @transaction.atomic
#     def confirm(self, request, *args, **kwargs):
#         teams = request.user.teams
#         order_id = request.data.get('id')
#         if not order_id:
#             raise ValidationError

#         purchase_order = PurchaseOrder.objects.filter(teams=teams, is_done=False, id=order_id).first()
#         if not purchase_order:
#             raise ValidationError

#         # 同步仓库, 创建流水
#         flows = []
#         for purchase_goods in purchase_order.goods_set.all().iterator():
#             # print(purchase_goods.goods, purchase_order.warehouse)
#             print(list(Inventory.objects.all()))
#             inventory = Inventory.objects.filter(teams=teams, goods=purchase_goods.goods,
#                                                  warehouse=purchase_order.warehouse).first()
#             if not inventory:
#                 raise APIException({'message': '表单已失效 (仓库/门店 或 商品 已被删除)'})
#             change_quantity = -purchase_goods.quantity if purchase_order.is_return else purchase_goods.quantity
#             inventory.quantity = math.plus(inventory.quantity, change_quantity)
#             inventory.save()

#             type = '采购退货单' if purchase_order.is_return else '采购单'
#             flows.append(Flow(type=type, teams=teams, goods=purchase_goods.goods, goods_number=purchase_goods.number,
#                               goods_name=purchase_goods.name,
#                               unit=purchase_goods.unit, warehouse=purchase_order.warehouse,
#                               warehouse_name=purchase_order.warehouse_name, change_quantity=change_quantity,
#                               remain_quantity=inventory.quantity, operator=request.user,
#                               operator_name=request.user.name, purchase_order=purchase_order))

#         Flow.objects.bulk_create(flows)

#         purchase_order.is_done = True
#         purchase_order.save()
#         return Response(status=HTTP_201_CREATED)

#     @action(detail=False)
#     @transaction.atomic
#     def payment(self, request, *args, **kwargs):
#         teams = request.user.teams
#         order_id = request.data.get('id')
#         amount = request.data.get('amount')
#         account = request.data.get('account')
#         remark = request.data.get('remark')

#         # 验证
#         if not order_id or not account or amount is None:
#             raise ValidationError
#         if amount <= 0:
#             raise ValidationError({'message': '金额错误'})

#         order = PurchaseOrder.objects.filter(teams=teams, id=order_id).first()
#         account = Account.objects.filter(teams=teams, id=account).first()
#         if not order or not account:
#             raise ValidationError
#         if order.amount + amount > order.total_amount:
#             raise ValidationError({'message': '金额已超出'})

#         PaymentRecord.objects.create(amount=amount, account=account, account_name=account.name,
#                                      purchase_order=order, remark=remark)
#         order.amount = math.plus(order.amount, amount)
#         order.save()
#         return Response({'id': order.id, 'amount': order.amount}, status=HTTP_201_CREATED)


class PurchasePaymentRecordViewSet(viewsets.ModelViewSet):
    """采购支付记录: list"""
    serializer_class = PurchasePaymentRecordSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PurchasePaymentRecordPagination
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_class = PurchasePaymentRecordFilter
    ordering_fields = ['purchase_order', 'date', 'amount']
    ordering = ['-date']

    def get_queryset(self):
        return PaymentRecord.objects.filter(purchase_order__teams=self.request.user.teams)


class PurchasePriceRecordViewSet(viewsets.ModelViewSet):
    """采购价变更记录: list"""
    serializer_class = PurchasePriceRecordSerializer
    permission_classes = [IsAuthenticated, PurchasePricePermission]
    pagination_class = PurchasePriceRecordPagination
    filter_backends = [OrderingFilter]
    ordering_fields = ['create_datetime', 'goods_number', 'goods_name', 'before_change',
                       'after_change', 'operator']
    ordering = ['-create_datetime']

    def get_queryset(self):
        return self.request.user.teams.change_records.all()
