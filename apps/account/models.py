from django_mysql.models import JSONField
from django.db import models


class Role(models.Model):
    """角色"""
    name = models.CharField(max_length=48)
    remark = models.CharField(max_length=48, null=True, blank=True)
    permissions = JSONField()
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='roles')


class Account(models.Model):
    """结算账户"""
    TYPE = (('cash', '现金'), ('bank_account', '银行账户'), ('alipay', '支付宝'),
            ('wechat_pay', '微信支付'), ('other', '其他'))

    number = models.CharField(max_length=32)
    name = models.CharField(max_length=64)
    type = models.CharField(max_length=12, default='cash', choices=TYPE)
    remark = models.CharField(max_length=256, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='accounts')


class Bookkeeping(models.Model):
    """记账"""
    create_datetime = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey('account.Account', models.SET_NULL, related_name='bookkeeping_set', null=True)
    account_name = models.CharField(max_length=64)
    amount = models.FloatField(default=0)  # 收入支出
    recorder = models.ForeignKey('user.User', models.SET_NULL, related_name='bookkeeping_set', null=True)
    recorder_name = models.CharField(max_length=64)
    remark = models.CharField(max_length=64, null=True, blank=True)
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='bookkeeping_set')
