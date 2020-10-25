from django.db import models


class Supplier(models.Model):
    """供应商"""
    number = models.CharField(max_length=32)
    name = models.CharField(max_length=64)
    contacts = models.CharField(max_length=64, null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    email = models.CharField(max_length=256, null=True, blank=True)
    address = models.CharField(max_length=256, null=True, blank=True)
    remark = models.CharField(max_length=256, null=True, blank=True)
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='suppliers')


class PurchaseOrder(models.Model):
    """采购单/采购退货单"""
    number = models.CharField(max_length=32)
    supplier = models.ForeignKey('purchase.Supplier', models.SET_NULL, related_name='purchase_orders', null=True)  # 供应商
    supplier_name = models.CharField(max_length=64)
    warehouse = models.ForeignKey('warehouse.Warehouse', models.SET_NULL, related_name='purchase_orders', null=True)
    warehouse_name = models.CharField(max_length=64)
    warehouse_address = models.CharField(max_length=256, null=True, blank=True)
    account = models.ForeignKey('account.Account', models.SET_NULL, related_name='purchase_orders', null=True)  # 结算账户
    account_name = models.CharField(max_length=64)
    contacts = models.ForeignKey('user.User', models.SET_NULL, related_name='purchase_orders', null=True)  # 联系人
    contacts_name = models.CharField(max_length=64)
    contacts_phone = models.CharField(max_length=12)
    amount = models.FloatField(default=0)  # 实付金额
    total_amount = models.FloatField(default=0)  # 应收金额
    total_quantity = models.FloatField(default=0)  # 总数量
    date = models.DateTimeField()
    remark = models.CharField(max_length=64, null=True, blank=True)
    # is_done = models.BooleanField(default=False)
    is_commit = models.BooleanField(default=False)
    # is_return = models.BooleanField(default=False)  # 退货单
    # purchase_order = models.ForeignKey('purchase.PurchaseOrder', models.CASCADE, related_name='return_order_set', null=True)
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='purchase_orders')


class PurchaseGoods(models.Model):
    """采购商品"""
    number = models.CharField(max_length=32)
    name = models.CharField(max_length=256)
    unit = models.CharField(max_length=32, null=True, blank=True)  # 单位
    purchase_price = models.FloatField(default=0)
    quantity = models.FloatField(default=0)
    amount = models.FloatField(default=0)  # 金额
    discount = models.FloatField(default=0)  # 折扣
    discount_price = models.FloatField(default=0)  # 折扣价
    discount_amount = models.FloatField(default=0)  # 折扣金额
    goods = models.ForeignKey('goods.Goods', models.SET_NULL, related_name='purchase_goods_set', null=True)
    purchase_order = models.ForeignKey('purchase.PurchaseOrder', models.CASCADE, related_name='goods_set')
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='purchase_goods_set')


class PaymentRecord(models.Model):
    """付款记录"""
    date = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField(default=0)
    purchase_order = models.ForeignKey('purchase.PurchaseOrder', models.CASCADE, related_name='payment_records')
    account = models.ForeignKey('account.Account', models.SET_NULL, related_name='purchase_payment_records', null=True)  # 结算账户
    account_name = models.CharField(max_length=64)
    remark = models.CharField(max_length=256, null=True, blank=True)


class PurchasePriceRecord(models.Model):
    """采购价历史记录"""
    create_datetime = models.DateTimeField(auto_now_add=True)
    goods = models.ForeignKey('goods.Goods', models.SET_NULL, related_name='change_records', null=True)
    goods_number = models.CharField(max_length=32)
    goods_name = models.CharField(max_length=256)
    before_change = models.FloatField()
    after_change = models.FloatField()
    operator = models.ForeignKey('user.User', models.SET_NULL, related_name='change_records', null=True)
    operator_name = models.CharField(max_length=64)
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='change_records')
