from number_precision.number_precision import NP
from .permissions import WarehousePermission, InventoryPermission, FlowPermission, CountingListPermission, RequisitionPermission
from .serializers import WarehouseSerializer, FlowSerializer, CountingListSerializer, RequisitionSerializer, InventorySerializer
from .paginations import FlowPagination, CountingListPagination, RequisitionPagination, InventoryPagination, WarehousePagination
from utils.permissions import IsAuthenticated, PurchasePricePermission
from rest_framework.exceptions import APIException, ValidationError
from .models import CountingListGoods, RequisitionGoods, StockInGoods, Warehouse
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import F, Sum, Q, Count, Value
from .filters import FlowFilter, InventoryFilter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.warehouse.models import Inventory, Flow
from rest_framework.decorators import action
from django.db import models, transaction
from django.http import HttpResponse
from rest_framework import viewsets
from apps.goods.models import Goods
from utils import math
import pendulum
import csv
from .serializers import WarehouseUpdateSerializer
from utils.excel import export_excel, import_excel
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from apps.warehouse.serializers import StockInOrderSerializer, StockInGoodsSerializer
from apps.warehouse.paginations import StockInOrderPagination
from apps.warehouse.models import Batch


class WarehouseViewSet(viewsets.ModelViewSet):
    """仓库: list, create, update, destroy"""
    serializer_class = WarehouseSerializer
    pagination_class = WarehousePagination
    permission_classes = [IsAuthenticated, WarehousePermission]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filter_fields = ['is_active']
    search_fields = ['number', 'name', 'address', 'remark']
    ordering_fields = ['number', 'name']
    ordering = ['number']
    field_mapping = (('number', '编号'), ('name', '名称'), ('address', '地址'),
                     ('remark', '备注'), ('is_active', '状态'))

    def get_serializer_class(self):
        return WarehouseUpdateSerializer if self.request.method == 'PUT' else self.serializer_class

    def get_queryset(self):
        return self.request.user.teams.warehouses.all()

    @transaction.atomic
    def perform_create(self, serializer):
        serializer.save(teams=self.request.user.teams)
        Inventory.objects.bulk_create(self.create_inventory(serializer.instance))

    @action(detail=False)
    def export_excel(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return export_excel(serializer.data, '仓库列表', self.field_mapping)

    @action(detail=False)
    @transaction.atomic
    def import_excel(self, request, *args, **kwargs):
        teams = request.user.teams
        warehouses = Warehouse.objects.bulk_create([Warehouse(**item, teams=teams)
                                                    for item in import_excel(self, self.field_mapping)])
        # 同步库存
        warehouse_numbers = [warehouse.number for warehouse in warehouses]
        warehouses = Warehouse.objects.filter(number__in=warehouse_numbers, teams=teams)
        for warehouse in warehouses:
            Inventory.objects.bulk_create(self.create_inventory(warehouse))

        return Response(status=HTTP_201_CREATED)

    def create_inventory(self, warehouse):
        teams = self.request.user.teams
        for goods in Goods.objects.filter(teams=teams).iterator():
            yield Inventory(warehouse=warehouse, goods=goods, teams=teams)


class InventoryViewSet(viewsets.ModelViewSet):
    """list"""
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated, InventoryPermission, PurchasePricePermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = InventoryFilter
    pagination_class = InventoryPagination

    def get_queryset(self):
        return self.request.user.teams.inventories.all()

    @action(detail=False)
    def export(self, request, *args, **kwargs):
        queryset = InventoryFilter(request.GET)
        if not queryset.is_valid():
            raise ValidationError

        queryset = queryset.filter_queryset(request.user.teams.inventories.all())
        results = queryset.all().values('quantity', number=F('goods__number'), name=F('goods__name'), brand=F('goods__brand'),
                                        category_name=F('goods__category__name'),
                                        unit=F('goods__unit'), purchase_price=F('goods__purchase_price'),
                                        warehouse_name=F('warehouse__name'))

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment;filename=inventory.csv'

        writer = csv.DictWriter(response, ['number', 'name', 'brand', 'unit', 'category_name',
                                           'warehouse_name', 'quantity', 'purchase_price'])
        writer.writeheader()
        writer.writerows(results)
        return response


class FlowViewSet(viewsets.ModelViewSet):
    """list"""
    serializer_class = FlowSerializer
    permission_classes = [IsAuthenticated, FlowPermission]
    pagination_class = FlowPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = FlowFilter
    search_fields = ['goods_number', 'goods_name']
    ordering_fields = ['create_datetime', 'goods_number', 'goods_name', 'change_quantity', 'remain_quantity']
    ordering = ['-create_datetime']

    def get_queryset(self):
        return self.request.user.teams.flows.all()


class CountingListViewSet(viewsets.ModelViewSet):
    """list, create, retrieve"""
    serializer_class = CountingListSerializer
    permission_classes = [IsAuthenticated, CountingListPermission, PurchasePricePermission]
    pagination_class = CountingListPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filter_fields = ['warehouse']
    search_fields = ['id', 'remark']
    ordering_fields = ['id', 'date']
    ordering = ['-id']

    def get_queryset(self):
        return self.request.user.teams.counting_list_set.all()

    @transaction.atomic
    def perform_create(self, serializer):
        order_id = f'C{pendulum.now().format("YYYYMMDDHHmmssSSSS")}'
        teams = self.request.user.teams

        # 验证
        warehouse = self.request.data.get('warehouse')
        warehouse = Warehouse.objects.filter(id=warehouse, teams=teams).first()
        if not warehouse:
            raise ValidationError

        # 创建表单商品, 同步仓库, 创建流水
        goods_set = self.request.data.get('goods_set', [])
        goods_id_set = map(lambda item: item['id'], goods_set)
        goods_list = Goods.objects.filter(id__in=goods_id_set, teams=teams)

        if len(goods_set) != len(goods_list):
            raise ValidationError

        flows = []
        counting_goods_set = []
        total_quantity = 0
        profit_quantity = 0
        profit_amount = 0
        for goods1 in goods_list:
            for goods2 in goods_set:
                if goods1.id == goods2['id']:
                    inventory = Inventory.objects.filter(teams=teams, goods=goods1, warehouse=warehouse).first()
                    if not inventory:
                        raise APIException

                    change_quantity = goods2['quantity'] - inventory.quantity
                    total_quantity = math.plus(total_quantity, goods2['quantity'])
                    profit_quantity = math.plus(profit_quantity, change_quantity)
                    profit_amount = math.plus(profit_amount, math.times(change_quantity, goods1.purchase_price))

                    counting_goods_set.append(CountingListGoods(goods=goods1, number=goods1.number, name=goods1.name,
                                                                unit=goods1.unit,
                                                                quantity=goods2['quantity'], before_counting=inventory.quantity,
                                                                purchase_price=goods1.purchase_price, counting_list_id=order_id))

                    flows.append(Flow(type='盘点单', teams=teams, goods=goods1, goods_number=goods1.number,
                                      goods_name=goods1.name,
                                      unit=goods1.unit, warehouse=warehouse, warehouse_name=warehouse.name,
                                      change_quantity=change_quantity, remain_quantity=goods2['quantity'],
                                      operator=self.request.user,
                                      operator_name=self.request.user.name, counting_list_id=order_id))

                    inventory.quantity = goods2['quantity']
                    inventory.save()
                    break

        serializer.save(id=order_id, warehouse_name=warehouse.name, total_quantity=total_quantity,
                        profit_quantity=profit_quantity, profit_amount=profit_amount, teams=teams)
        CountingListGoods.objects.bulk_create(counting_goods_set)
        Flow.objects.bulk_create(flows)


class RequisitionViewSet(viewsets.ModelViewSet):
    """list, create, update, destroy"""
    serializer_class = RequisitionSerializer
    permission_classes = [IsAuthenticated, RequisitionPermission]
    pagination_class = RequisitionPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filter_fields = ['out_warehouse', 'into_warehouse']
    search_fields = ['id', 'remark']
    ordering_fields = ['id', 'date']
    ordering = ['-id', 'date']

    def get_queryset(self):
        return self.request.user.teams.requisition_set.all()

    @transaction.atomic
    def perform_create(self, serializer):
        order_id = f'R{pendulum.now().format("YYYYMMDDHHmmssSSSS")}'
        teams = self.request.user.teams

        # 验证
        out_warehouse = self.request.data.get('out_warehouse')
        out_warehouse = Warehouse.objects.filter(id=out_warehouse, teams=teams).first()
        into_warehouse = self.request.data.get('into_warehouse')
        into_warehouse = Warehouse.objects.filter(id=into_warehouse, teams=teams).first()
        if not out_warehouse or not into_warehouse:
            raise ValidationError

        # 创建表单商品, 同步仓库, 创建流水
        goods_set = self.request.data.get('goods_set', [])
        goods_id_set = map(lambda item: item['id'], goods_set)
        goods_list = Goods.objects.filter(id__in=goods_id_set, teams=teams)

        if len(goods_set) != len(goods_list):
            raise ValidationError

        flows = []
        requisition_goods_set = []
        total_quantity = 0
        for goods1 in goods_list:
            for goods2 in goods_set:
                if goods1.id == goods2['id']:
                    out_inventory = Inventory.objects.filter(teams=teams, goods=goods1, warehouse=out_warehouse).first()
                    into_inventory = Inventory.objects.filter(teams=teams, goods=goods1, warehouse=into_warehouse).first()

                    if not out_inventory or not into_inventory:
                        raise APIException

                    change_quantity = goods2['quantity']
                    out_inventory.quantity = math.minus(out_inventory.quantity, change_quantity)
                    into_inventory.quantity = math.plus(into_inventory.quantity, change_quantity)
                    out_inventory.save()
                    into_inventory.save()
                    total_quantity = math.plus(total_quantity, goods2['quantity'])

                    requisition_goods_set.append(RequisitionGoods(goods=goods1, number=goods1.number, name=goods1.name,
                                                                  unit=goods1.unit,
                                                                  quantity=goods2['quantity'],
                                                                  requisition_id=order_id))

                    flows.append(Flow(type='调拨单', teams=teams, goods=goods1, goods_number=goods1.number,
                                      goods_name=goods1.name,
                                      unit=goods1.unit, warehouse=out_warehouse, warehouse_name=out_warehouse.name,
                                      change_quantity=-change_quantity, remain_quantity=out_inventory.quantity,
                                      operator=self.request.user, operator_name=self.request.user.name,
                                      requisition_id=order_id))
                    flows.append(Flow(type='调拨单', teams=teams, goods=goods1, goods_number=goods1.number,
                                      goods_name=goods1.name,
                                      unit=goods1.unit, warehouse=into_warehouse, warehouse_name=into_warehouse.name,
                                      change_quantity=change_quantity, remain_quantity=into_inventory.quantity,
                                      operator=self.request.user, operator_name=self.request.user.name,
                                      requisition_id=order_id))
                    break

        serializer.save(id=order_id, out_warehouse_name=out_warehouse.name, total_quantity=total_quantity,
                        into_warehouse_name=into_warehouse.name, teams=teams)

        RequisitionGoods.objects.bulk_create(requisition_goods_set)
        Flow.objects.bulk_create(flows)


class StockInOrderViewSet(viewsets.ModelViewSet):
    """入库单据: list"""
    serializer_class = StockInOrderSerializer
    pagination_class = StockInOrderPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filter_fields = ['warehouse', 'is_complete']
    search_fields = ['number']
    ordering_fields = ['number', 'create_date']
    ordering = ['-number', 'create_date']

    def get_queryset(self):
        return self.request.user.teams.stock_in_orders.all()


class StockInGoodsViewSet(viewsets.ModelViewSet):
    """入库商品"""
    serializer_class = StockInGoodsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.teams.stock_in_goods_set.select_related('stock_in_order', 'goods').all()

    @action(detail=True)
    @transaction.atomic
    def stock_in(self, request, *args, **kwargs):
        stock_in_goods = self.get_object()
        quantity = request.data.get('quantity', 0)
        if quantity <= 0:
            raise APIException('入库数量不能小于0')

        quantity_completed = NP.plus(stock_in_goods.quantity_completed, quantity)
        if quantity_completed > stock_in_goods.quantity:
            raise APIException('入库数量异常')

        stock_in_goods.quantity_completed = quantity_completed
        stock_in_goods.save()

        if not StockInGoods.objects.filter(stock_in_order=stock_in_goods.stock_in_order,
                                           quantity_completed__gte=F('quantity')).exists():
            stock_in_goods.stock_in_order.is_complete = True
            stock_in_goods.stock_in_order.save()

        # 同步库存
        inventory = self.get_inventory(stock_in_goods)
        batch = self.create_batch(stock_in_goods, quantity)
        if batch:
            inventory.batchs.add(batch)

        inventory.quantity = NP.plus(inventory.quantity, quantity)
        inventory.save()
        return Response(self.get_serializer(stock_in_goods).data)

    def get_inventory(self, stock_in_goods):
        warehouse = stock_in_goods.stock_in_order.warehouse
        if not warehouse:
            raise APIException('仓库不存在')

        goods = stock_in_goods.goods
        if not goods:
            raise APIException('商品不存在')

        inventory = Inventory.objects.filter(teams=self.request.user.teams, warehouse=warehouse,
                                             goods=goods).first()
        if not inventory:
            raise APIException('库存不存在')

        return inventory

    def create_batch(self, stock_in_goods, quantity):
        if stock_in_goods.goods.shelf_life_warnning:
            production_date = self.request.data.get('production_date')
            if production_date is None:
                raise APIException('生产日期不能为空')
            return Batch.objects.create(goods=stock_in_goods.goods, production_date=production_date,
                                        quantity=quantity, teams=self.request.user.teams)
        return None
