from django.db import models


class SalesOrder(models.Model):
    """销售单"""
    id = models.CharField(primary_key=True, max_length=20)
    date = models.DateTimeField()
    seller = models.ForeignKey('user.User', models.SET_NULL, related_name='sales_order_set', null=True)  # 销售员
    seller_name = models.CharField(max_length=48)
    warehouse = models.ForeignKey('warehouse.Warehouse', models.SET_NULL, related_name='sales_order_set', null=True)
    warehouse_name = models.CharField(max_length=48)
    account = models.ForeignKey('account.Account', models.SET_NULL, related_name='sales_order_set', null=True)  # 结算账户
    account_name = models.CharField(max_length=48)
    discount = models.FloatField(default=100)  # 整单折扣
    amount = models.FloatField(default=0)  # 实收金额
    total_amount = models.FloatField(default=0)  # 应收金额
    total_quantity = models.FloatField(default=0)  # 总数量
    client = models.ForeignKey('sales.Client', models.SET_NULL, related_name='sales_order_set', null=True)
    client_name = models.CharField(max_length=64, null=True, blank=True)
    remark = models.CharField(max_length=256, null=True, blank=True)
    is_done = models.BooleanField(default=False)
    is_return = models.BooleanField(default=False)  # 退货单
    sales_order = models.ForeignKey('sales.SalesOrder', models.CASCADE, related_name='return_order_set', null=True)
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='sales_order_set')


class SalesGoods(models.Model):
    """销售商品"""
    number = models.CharField(max_length=32)
    name = models.CharField(max_length=256)
    unit = models.CharField(max_length=16, null=True, blank=True)  # 单位
    quantity = models.FloatField(default=0)
    purchase_price = models.FloatField(default=0)
    retail_price = models.FloatField(default=0)  # 单价
    amount = models.FloatField(default=0)  # 金额
    remark = models.CharField(max_length=256, null=True, blank=True)
    goods = models.ForeignKey('goods.Goods', models.SET_NULL, related_name='sales_goods_set', null=True)
    sales_order = models.ForeignKey('sales.SalesOrder', models.CASCADE, related_name='goods_set')


class PaymentRecord(models.Model):
    """付款记录"""
    date = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField(default=0)
    sales_order = models.ForeignKey('sales.SalesOrder', models.CASCADE, related_name='payment_records')
    account = models.ForeignKey('account.Account', models.SET_NULL, related_name='sales_payment_records', null=True)  # 结算账户
    account_name = models.CharField(max_length=64)
    remark = models.CharField(max_length=64, null=True, blank=True)


class SalesTask(models.Model):
    """销售任务"""
    goods = models.ForeignKey('goods.Goods', models.CASCADE, related_name='sales_tasks')
    warehouse = models.ForeignKey('warehouse.Warehouse', models.CASCADE, related_name='sales_tasks')
    quantity = models.FloatField(default=0)  # 任务数量
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    create_date = models.DateTimeField(auto_now_add=True)
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='sales_tasks')


class Client(models.Model):
    """客户"""
    number = models.CharField(max_length=32)
    name = models.CharField(max_length=64, null=True, blank=True)
    contacts = models.CharField(max_length=64, null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    email = models.CharField(max_length=256, null=True, blank=True)
    address = models.CharField(max_length=256, null=True, blank=True)
    remark = models.CharField(max_length=256, null=True, blank=True)
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='clients')
