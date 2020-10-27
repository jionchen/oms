from .serializers import SalesOrderSerializer, SalesTaskSerializer, ClientSerializer, SalesOrderProfitSerializer, SalesPaymentRecordSerializer
from .paginations import SalesOrderPagination, SalesTaskPagination, ClientPagination, SalesOrderProfitPagination, SalesPaymentRecordPagination
from utils.permissions import IsAuthenticated, PurchasePricePermission
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .filters import SalesTaskFilter, SalesOrderProfitFilter, SalesPaymentRecordFilter
from .models import SalesGoods, SalesOrder, PaymentRecord
from apps.warehouse.models import Inventory, Warehouse, Flow
from rest_framework.status import HTTP_201_CREATED
from rest_framework.exceptions import APIException
from .permissions import SalesOrderPermission
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from datetime import datetime, timedelta
from django.db.models import F, Sum
from apps.account.models import Account
from django.db import transaction
from apps.sales.models import Client
from apps.goods.models import Goods
from apps.user.models import User
from utils import math
import pendulum
from .serializers import ClientUpdateSerializer
from utils.excel import export_excel, import_excel
from number_precision import NP
import itertools
from apps.warehouse.models import StockOutOrder, StockOutGoods


class SalesOrderViewSet(viewsets.ModelViewSet):
    """销售单据: list, create, destroy, commit"""
    serializer_class = SalesOrderSerializer
    pagination_class = SalesOrderPagination
    permission_classes = [IsAuthenticated, SalesOrderPermission]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filter_fields = ['warehouse', 'seller', 'account', 'client', 'is_commit']
    search_fields = ['number', 'remark']
    ordering_fields = ['number', 'date']
    ordering = ['-number']

    def get_queryset(self):
        return self.request.user.teams.sales_orders.all()

    @transaction.atomic
    def perform_create(self, serializer):
        teams = self.request.user.teams
        order_number = self.create_sales_number()

        # 验证外键
        seller_username = self.request.data.get('seller')
        seller = User.objects.filter(teams=teams, username=seller_username).first()
        warehouse_id = self.request.data.get('warehouse')
        warehouse = Warehouse.objects.filter(teams=teams, id=warehouse_id).first()
        account_id = self.request.data.get('account')
        account = Account.objects.filter(teams=teams, id=account_id).first()
        client_id = self.request.data.get('client')
        client = Client.objects.filter(teams=teams, id=client_id).first() if client_id else None

        print(self.request.data)
        if not all([seller, warehouse, account]):
            raise APIException('销售员, 仓库, 账户, 客户不存在')

        # 创建销售表单
        serializer.save(teams=teams, number=order_number, seller_name=seller.name,
                        warehouse_name=warehouse.name, account_name=account.name,
                        client_name=client.name if client else None,
                        client_phone=client.phone if client else None,
                        client_address=client.address if client else None)

        # 创建销售商品
        SalesGoods.objects.bulk_create(self.create_goods(serializer.instance))

    def perform_destroy(self, instance):
        if instance.is_commit:
            raise APIException('销售单据已确认提交不能删除')
        instance.delete()

    @action(detail=True)
    @transaction.atomic
    def commit(self, request, *args, **kwargs):
        order = self.get_sales_order(kwargs.get('pk'))
        print(order)
        # 创建出库单据
        stock_out_order = StockOutOrder.objects.create(number=self.create_stock_out_number(), warehouse=order.warehouse,
                                                       warehouse_name=order.warehouse_name, teams=request.user.teams)

        stock_out_goods_set = []
        for sales_goods in order.goods_set.all():
            if not sales_goods.goods:
                raise APIException(f'商品[{sales_goods.goods_name}] 不存在')

            # 统计商品数量, 应收金额
            order.total_quantity = NP.plus(order.total_quantity, sales_goods.quantity)
            order.total_amount = NP.times(NP.plus(order.total_amount, sales_goods.amount), order.discount, 0.01)

            # 创建出库商品
            stock_out_goods_set.append(StockOutGoods(stock_out_order=stock_out_order, goods=sales_goods.goods,
                                                     goods_number=sales_goods.number, goods_name=sales_goods.name,
                                                     goods_unit=sales_goods.unit, quantity=sales_goods.quantity,
                                                     teams=request.user.teams))
        StockOutGoods.objects.bulk_create(stock_out_goods_set)

        order.is_commit = True
        order.save()
        return Response(self.get_serializer(order).data)

    def get_sales_order(self, pk):
        teams = self.request.user.teams
        order = SalesOrder.objects.prefetch_related('goods_set').filter(teams=teams, pk=pk).first()
        if not order:
            raise APIException('单据不存在')

        if order.is_commit:
            raise APIException('销售单已提交出库')

        if not order.warehouse:
            raise APIException(f'仓库[{order.warehouse_name}] 不存在')

        return order

    def create_sales_number(self):
        return f'P{pendulum.now().format("YYYYMMDDHHmmssSSSSS")}'

    def create_stock_out_number(self):
        return f'SO{pendulum.now().format("YYYYMMDDHHmmssSSSS")}'

    def create_goods(self, sales_order):
        teams = self.request.user.teams
        goods_set = self.request.data.get('goods_set', [])
        goods_ids = map(lambda item: item['id'], goods_set)
        goods_list = Goods.objects.filter(id__in=goods_ids, teams=teams)

        if len(goods_set) != len(goods_list):
            raise APIException('商品不存在')

        for item in itertools.product(goods_list, goods_set):
            if item[0].id == item[1]['id']:
                quantity, retail_price = (item[1].get('quantity'), item[1].get('retail_price'))
                if retail_price < 0 or quantity <= 0:
                    raise APIException('商品数据异常')

                yield SalesGoods(teams=teams, sales_order=sales_order, goods=item[0], number=item[0].number,
                                 name=item[0].name, unit=item[0].unit, quantity=quantity,
                                 purchase_price=item[0].purchase_price, retail_price=retail_price,
                                 amount=NP.times(retail_price, quantity))


# class SalesOrderViewSet(viewsets.ModelViewSet):
#     """list, create, destroy"""
#     serializer_class = SalesOrderSerializer
#     permission_classes = [IsAuthenticated, SalesOrderPermission]
#     pagination_class = SalesOrderPagination
#     filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
#     filterset_class = SalesOrderFilter
#     search_fields = ['id', 'client_name', 'client_phone', 'remark']
#     ordering_fields = ['id', 'date', 'total_amount', 'amount']
#     ordering = ['-id']

#     def get_queryset(self):
#         return self.request.user.teams.sales_orders.all()

#     @transaction.atomic
#     def perform_create(self, serializer):
#         order_id = f'S{pendulum.now().format("YYYYMMDDHHmmssSSSS")}'
#         teams = self.request.user.teams

#         # 验证
#         if self.request.data.get('is_return', False):  # 退货单
#             sales_order = self.request.data.get('sales_order')
#             sales_order = SalesOrder.objects.filter(
#                 id=sales_order, is_done=True, is_return=False, teams=teams).first()
#             if not sales_order:
#                 raise ValidationError
#             warehouse = sales_order.warehouse
#         else:
#             warehouse = self.request.data.get('warehouse')
#             warehouse = Warehouse.objects.filter(id=warehouse, teams=teams).first()

#         seller = self.request.data.get('seller')
#         if seller == self.request.user.username:
#             seller = self.request.user
#         else:
#             seller = User.objects.filter(username=seller, teams=teams).first()

#         account = self.request.data.get('account')
#         account = Account.objects.filter(id=account, teams=teams).first()

#         if not warehouse or not account or not seller:
#             raise ValidationError

#         # 创建表单商品
#         goods_set = self.request.data.get('goods_set', [])
#         goods_id_set = map(lambda item: item['id'], goods_set)
#         goods_list = Goods.objects.filter(id__in=goods_id_set, teams=teams)

#         if len(goods_set) != len(goods_list):
#             raise ValidationError

#         discount = self.request.data.get('discount', 100)
#         total_quantity = 0
#         total_amount = 0
#         sales_goods_set = []
#         for goods1 in goods_list:
#             for goods2 in goods_set:
#                 if goods1.id == goods2['id']:
#                     amount = math.times(goods2['quantity'], goods2['retail_price'], discount, 0.01)
#                     total_quantity = math.plus(total_quantity, goods2['quantity'])
#                     total_amount = math.plus(total_amount, amount)

#                     sales_goods_set.append(
#                         SalesGoods(goods=goods1, number=goods1.number, name=goods1.name, unit=goods1.unit,
#                                    quantity=goods2['quantity'],
#                                    purchase_price=goods1.purchase_price, retail_price=goods2['retail_price'],
#                                    amount=amount, remark=goods2.get('remark'), sales_order_id=order_id))
#                     break

#         client = self.request.data.get('client')
#         client = Client.objects.filter(id=client, teams=teams).first() if client else None
#         client_name = client.name if client else None

#         serializer.save(teams=teams, id=order_id, seller_name=seller.name, warehouse_name=warehouse.name,
#                         account_name=account.name, total_quantity=total_quantity, total_amount=total_amount,
#                         client=client, client_name=client_name)
#         SalesGoods.objects.bulk_create(sales_goods_set)

#         # 创建付款记录
#         amount = self.request.data.get('amount', 0)
#         if amount != 0:
#             PaymentRecord.objects.create(amount=amount, account=account, account_name=account.name,
#                                          sales_order=serializer.instance)

#     @action(detail=False)
#     @transaction.atomic
#     def confirm(self, request, *args, **kwargs):
#         teams = request.user.teams
#         order_id = request.data.get('id')
#         if not order_id:
#             raise ValidationError

#         sales_order = SalesOrder.objects.filter(teams=teams, is_done=False, id=order_id).first()
#         if not sales_order:
#             raise ValidationError

#         # 同步仓库, 创建流水
#         flows = []
#         for sales_goods in sales_order.goods_set.all().iterator():
#             inventory = Inventory.objects.filter(
#                 teams=teams, goods=sales_goods.goods, warehouse=sales_order.warehouse).first()
#             if not inventory:
#                 raise APIException({'message': '表单已失效 (仓库/门店 或 商品 已被删除)'})
#             change_quantity = sales_goods.quantity if sales_order.is_return else -sales_goods.quantity
#             inventory.quantity = math.plus(inventory.quantity, change_quantity)
#             inventory.save()

#             type = '销售退货单' if sales_order.is_return else '销售单'
#             flows.append(Flow(type=type, teams=teams, goods=sales_goods.goods, goods_number=sales_goods.number,
#                               goods_name=sales_goods.name,
#                               unit=sales_goods.unit, warehouse=sales_order.warehouse,
#                               warehouse_name=sales_order.warehouse_name, change_quantity=change_quantity,
#                               remain_quantity=inventory.quantity, operator=request.user,
#                               operator_name=request.user.name, sales_order=sales_order))

#         Flow.objects.bulk_create(flows)

#         sales_order.is_done = True
#         sales_order.save()
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

#         order = SalesOrder.objects.filter(teams=teams, id=order_id).first()
#         account = Account.objects.filter(teams=teams, id=account).first()
#         if not order or not account:
#             raise ValidationError
#         if order.amount + amount > order.total_amount:
#             raise ValidationError({'message': '金额已超出'})

#         PaymentRecord.objects.create(amount=amount, account=account, account_name=account.name,
#                                      sales_order=order, remark=remark)
#         order.amount = math.plus(order.amount, amount)
#         order.save()
#         return Response({'id': order.id, 'amount': order.amount}, status=HTTP_201_CREATED)


class SalesPaymentRecordViewSet(viewsets.ModelViewSet):
    """销售支付记录: list"""
    serializer_class = SalesPaymentRecordSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = SalesPaymentRecordPagination
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_class = SalesPaymentRecordFilter
    ordering_fields = ['sales_order', 'date', 'amount']
    ordering = ['-date']

    def get_queryset(self):
        return PaymentRecord.objects.filter(sales_order__teams=self.request.user.teams)


class SalesTaskViewSet(viewsets.ModelViewSet):
    """销售任务: list, create"""
    serializer_class = SalesTaskSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = SalesTaskPagination
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_class = SalesTaskFilter
    ordering_fields = ['create_date']
    ordering = ['-create_date']

    def get_queryset(self):
        return self.request.user.teams.sales_tasks.all()

    def perform_create(self, serializer):
        end_date = self.request.data['end_date']
        end_date = pendulum.parse(end_date).add(days=1)
        serializer.save(end_date=end_date, teams=self.request.user.teams)


class SalesOrderProfitViewSet(viewsets.ModelViewSet):
    """利润统计: list, update (修改成本)"""
    serializer_class = SalesOrderProfitSerializer
    permission_classes = [IsAuthenticated, PurchasePricePermission]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    pagination_class = SalesOrderProfitPagination
    filterset_class = SalesOrderProfitFilter
    search_fields = ['id']
    ordering_fields = ['id', 'date']
    ordering = ['-id']

    def get_queryset(self):
        return self.request.user.teams.sales_orders.filter(is_return=False)

    def update(self, request, *args, **kwargs):
        sales_goods_id = kwargs.get('pk')
        purchase_price = request.data.get('purchase_price')
        if not sales_goods_id or not purchase_price:
            raise ValidationError

        SalesGoods.objects.filter(
            sales_order__teams=request.user.teams, id=sales_goods_id).update(purchase_price=purchase_price)
        return Response(status=status.HTTP_200_OK)

    @action(detail=False)
    def total_profit(self, request, *args, **kwargs):
        warehouse = request.GET.get('warehouse')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        queryset = SalesGoods.objects.filter(sales_order__teams=request.user.teams, sales_order__is_return=False)
        if warehouse:
            queryset = queryset.filter(sales_order__warehouse_id=warehouse)
        if start_date:
            queryset = queryset.filter(sales_order__date__gte=start_date)
        if end_date:
            end_date = pendulum.parse(end_date).add(days=1)
            queryset = queryset.filter(sales_order__date__lte=end_date)

        total_profit = queryset.aggregate(total_profit=Sum(
            (F('retail_price') * F('sales_order__discount') * 0.01 - F('purchase_price')) * F('quantity'))).get('total_profit')
        return Response({'total_profit': total_profit if total_profit else 0})


class ClientViewSet(viewsets.ModelViewSet):
    """客户: list, create, update, destroy"""
    serializer_class = ClientSerializer
    pagination_class = ClientPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['number', 'name', 'phone', 'email', 'address', 'remark']
    ordering_fields = ['number', 'name']
    ordering = ['number']
    field_mapping = (('number', '编号'), ('name', '名称'), ('contacts', '联系人'), ('phone', '电话'),
                     ('email', '邮箱'), ('address', '地址'), ('remark', '备注'))

    def get_serializer_class(self):
        return ClientUpdateSerializer if self.request.method == 'PUT' else self.serializer_class

    def get_queryset(self):
        return self.request.user.teams.clients.all()

    def perform_create(self, serializer):
        serializer.save(teams=self.request.user.teams)

    @action(detail=False)
    def export_excel(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return export_excel(serializer.data, '客户列表', self.field_mapping)

    @action(detail=False)
    @transaction.atomic
    def import_excel(self, request, *args, **kwargs):
        Client.objects.bulk_create([Client(**item, teams=request.user.teams)
                                    for item in import_excel(self, self.field_mapping)])
        return Response(status=HTTP_201_CREATED)
