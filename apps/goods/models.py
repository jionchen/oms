from django.db import models


class Category(models.Model):
    """商品分类"""
    number = models.CharField(max_length=32)
    name = models.CharField(max_length=64)
    remark = models.CharField(max_length=256, null=True, blank=True)
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='categories')


class Goods(models.Model):
    """商品"""
    number = models.CharField(max_length=32)
    name = models.CharField(max_length=256)
    unit = models.CharField(max_length=32, null=True, blank=True)
    category = models.ForeignKey('goods.Category', models.SET_NULL, related_name='goods_set', null=True)
    purchase_price = models.FloatField(default=0)
    retail_price = models.FloatField(default=0)
    shelf_life_warnning = models.BooleanField(default=False)  # 保质期预警
    shelf_life = models.IntegerField(default=30)  
    shelf_life_warnning_days = models.IntegerField(default=0)  # 保质期预警天数
    inventory_warning = models.BooleanField(default=False)  # 库存预警
    inventory_upper = models.FloatField(default=100)
    inventory_lower = models.FloatField(default=0)
    remark = models.CharField(max_length=256, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='goods_set')
