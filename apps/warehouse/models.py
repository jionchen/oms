from django.db import models


class Warehouse(models.Model):
    """仓库"""
    number = models.CharField(max_length=32)
    name = models.CharField(max_length=64)
    address = models.CharField(max_length=256, null=True, blank=True)
    remark = models.CharField(max_length=256, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='warehouses')


class Inventory(models.Model):
    """库存"""
    goods = models.ForeignKey('goods.Goods', models.CASCADE, related_name='inventories')
    warehouse = models.ForeignKey('warehouse.Warehouse', models.CASCADE, related_name='inventories')
    batchs = models.ManyToManyField('warehouse.Batch', related_name='inventories', blank=True)
    quantity = models.FloatField(default=0)
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='inventories')


class Batch(models.Model):
    """批次"""
    create_date = models.DateTimeField(auto_now_add=True)
    goods = models.ForeignKey('goods.Goods', models.CASCADE, related_name='batchs')
    production_date = models.DateTimeField()
    quantity = models.FloatField()
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='batchs')


class Flow(models.Model):
    """库存流水"""
    create_datetime = models.DateTimeField(auto_now_add=True)
    goods = models.ForeignKey('goods.Goods', models.SET_NULL, related_name='flows', null=True)
    goods_name = models.CharField(max_length=256)
    unit = models.CharField(max_length=16, null=True, blank=True)  # 单位
    warehouse = models.ForeignKey('warehouse.Warehouse', models.SET_NULL, related_name='flows', null=True)
    warehouse_name = models.CharField(max_length=4648)
    change_quantity = models.FloatField(default=0)
    remain_quantity = models.FloatField(default=0)
    type = models.CharField(max_length=12)
    operator = models.ForeignKey('user.User', models.SET_NULL, related_name='flows', null=True)
    operator_name = models.CharField(max_length=64)
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='flows')

    # 关联单
    requisition = models.ForeignKey('warehouse.Requisition', models.CASCADE, related_name='flows', null=True)
    counting_list = models.ForeignKey('warehouse.CountingList', models.CASCADE, related_name='flows', null=True)
    purchase_order = models.ForeignKey('purchase.PurchaseOrder', models.CASCADE, related_name='flows', null=True)
    sales_order = models.ForeignKey('sales.SalesOrder', models.CASCADE, related_name='flows', null=True)


class StockInOrder(models.Model):
    """入库单据"""
    number = models.CharField(max_length=32)
    create_date = models.DateTimeField(auto_now_add=True)
    warehouse = models.ForeignKey('warehouse.Warehouse', models.SET_NULL, related_name='stock_in_orders', null=True)
    warehouse_name = models.CharField(max_length=64)
    is_complete = models.BooleanField(default=False)
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='stock_in_orders')


class StockInGoods(models.Model):
    """入库商品"""
    stock_in_order = models.ForeignKey('warehouse.StockInOrder', models.CASCADE, related_name='goods_set')
    goods = models.ForeignKey('goods.Goods', models.SET_NULL, related_name='stock_in_goods_set', null=True)
    goods_number = models.CharField(max_length=32)
    goods_name = models.CharField(max_length=256)
    goods_unit = models.CharField(max_length=32, null=True, blank=True)
    quantity = models.FloatField()
    quantity_completed = models.FloatField(default=0)
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='stock_in_goods_set')


class StockOutOrder(models.Model):
    """出库单据"""
    number = models.CharField(max_length=32)
    create_date = models.DateTimeField(auto_now_add=True)
    warehouse = models.ForeignKey('warehouse.Warehouse', models.SET_NULL, related_name='stock_out_orders', null=True)
    warehouse_name = models.CharField(max_length=64)
    is_complete = models.BooleanField(default=False)
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='stock_out_orders')


class StockOutGoods(models.Model):
    """出库商品"""
    stock_out_order = models.ForeignKey('warehouse.StockInOrder', models.CASCADE, related_name='stock_out_goods_set')
    goods = models.ForeignKey('goods.Goods', models.SET_NULL, related_name='stock_out_goods_set', null=True)
    goods_number = models.CharField(max_length=32)
    goods_name = models.CharField(max_length=256)
    goods_unit = models.CharField(max_length=32, null=True, blank=True)
    quantity = models.FloatField()
    quantity_completed = models.FloatField(default=0)
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='stock_out_goods_set')


class StockCheckOrder(models.Model):
    """盘点单据"""


class StockCheckGoods(models.Model):
    """盘点商品"""


class StockTransferOrder(models.Model):
    """调拨单据"""


class StockTransferGoods(models.Model):
    """调拨商品"""


class CountingList(models.Model):
    """盘点单"""
    id = models.CharField(primary_key=True, max_length=20)
    warehouse = models.ForeignKey('warehouse.Warehouse', models.SET_NULL, related_name='counting_list_set', null=True)
    warehouse_name = models.CharField(max_length=48)
    total_quantity = models.FloatField(default=0)  # 盘点总数
    profit_quantity = models.FloatField(default=0)
    profit_amount = models.FloatField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    remark = models.CharField(max_length=64, null=True, blank=True)
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='counting_list_set')


class CountingListGoods(models.Model):
    """盘点单商品"""
    number = models.CharField(max_length=32)
    name = models.CharField(max_length=256)
    unit = models.CharField(max_length=16, null=True, blank=True)  # 单位
    quantity = models.FloatField(default=0)  # 盘点数量
    before_counting = models.FloatField(default=0)  # 盘点前数量
    purchase_price = models.FloatField(default=0)
    goods = models.ForeignKey('goods.Goods', models.SET_NULL, related_name='counting_list_goods_set', null=True)
    counting_list = models.ForeignKey('warehouse.CountingList', models.CASCADE, related_name='goods_set')


class Requisition(models.Model):
    """调拨单"""
    id = models.CharField(primary_key=True, max_length=20)
    out_warehouse = models.ForeignKey('warehouse.Warehouse', models.SET_NULL, related_name='into_requisitions', null=True)
    out_warehouse_name = models.CharField(max_length=64)
    into_warehouse = models.ForeignKey('warehouse.Warehouse', models.SET_NULL, related_name='out_requisitions', null=True)
    into_warehouse_name = models.CharField(max_length=64)
    total_quantity = models.FloatField(default=0)  # 总数量
    date = models.DateTimeField()
    remark = models.CharField(max_length=64, null=True, blank=True)
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='requisition_set')


class RequisitionGoods(models.Model):
    """调拨单商品"""
    number = models.CharField(max_length=32)
    name = models.CharField(max_length=256)
    unit = models.CharField(max_length=16, null=True, blank=True)  # 单位
    quantity = models.FloatField(default=0)
    goods = models.ForeignKey('goods.Goods', models.SET_NULL, related_name='requisition_goods_set', null=True)
    requisition = models.ForeignKey('warehouse.Requisition', models.CASCADE, related_name='goods_set')
