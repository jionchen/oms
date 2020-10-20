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
    category = models.ForeignKey('goods.Category', models.CASCADE, related_name='goods_set', null=True)
    purchase_price = models.FloatField(default=0)
    retail_price = models.FloatField(default=0)
    shelf_life = models.FloatField(null=True)
    shelf_life_warnning_days = models.IntegerField(null=True)
    inventory_upper = models.FloatField(null=True)
    inventory_lower = models.FloatField(null=True)
    inventory_warning = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='goods_set')
