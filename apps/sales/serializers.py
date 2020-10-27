from .models import SalesOrder, SalesTask, Client, PaymentRecord
from rest_framework import serializers
from django.db.models import Sum, F
from apps.warehouse.models import Flow
import re


class SalesOrderSerializer(serializers.ModelSerializer):
    goods_set = serializers.SerializerMethodField('get_goods_set')

    class Meta:
        model = SalesOrder
        read_only_fields = ['id', 'number', 'seller_name', 'warehouse_name', 'account_name',
                            'client_name', 'client_phone', 'client_address', 'is_commit',
                            'goods_set', 'total_amount', 'total_quantity']
        fields = ['date', 'seller', 'warehouse', 'account', 'discount', 'amount',
                  'client', 'remark', *read_only_fields]

    def validate(self, data):
        print(data)
        if data.get('discount') is None or data['discount'] < 0:
            raise serializers.ValidationError({'discount': '整单折扣不能小于0'})

        if len(self.context['request'].data.get('goods_set', [])) == 0:
            raise serializers.ValidationError('表单商品不能为空')
        return data

    def get_goods_set(self, obj):
        return obj.goods_set.all().values('id', 'number', 'name', 'unit', 'quantity',
                                          'retail_price', 'amount')


class SalesPaymentRecordSerializer(serializers.ModelSerializer):
    client_name = serializers.SerializerMethodField('get_client_name')

    class Meta:
        model = PaymentRecord
        read_only_fields = ['sales_order', 'date', 'amount',  'remark', 'client_name']
        fields = [*read_only_fields]

    def get_client_name(self, obj):
        return obj.sales_order.client_name


class SalesOrderProfitSerializer(serializers.ModelSerializer):
    goods_set = serializers.SerializerMethodField('get_goods_set')

    class Meta:
        model = SalesOrder
        read_only_fields = ['id', 'date', 'warehouse',  'warehouse_name', 'discount', 'goods_set']
        fields = [*read_only_fields]

    def get_goods_set(self, obj):
        return obj.goods_set.all().values('id', 'number', 'name', 'unit', 'quantity',
                                          'retail_price', 'purchase_price', 'remark')


class SalesTaskSerializer(serializers.ModelSerializer):
    goods_name = serializers.SerializerMethodField('get_goods_name')
    warehouse_name = serializers.SerializerMethodField('get_warehouse_name')
    completed_quantity = serializers.SerializerMethodField('get_completed_quantity')

    class Meta:
        model = SalesTask
        fields = ['id', 'goods', 'goods_name', 'warehouse', 'warehouse_name', 'quantity',
                  'start_date', 'end_date', 'create_date', 'completed_quantity']
        read_only_fields = ['id', 'goods_name', 'warehouse_name', 'create_date', 'completed_quantity']

    def validate(self, data):
        if not data.get('goods') or not data.get('warehouse') or data.get('quantity') is None:
            raise serializers.ValidationError

        if not data.get('start_date') or not data.get('end_date'):
            raise serializers.ValidationError

        teams = self.context['request'].user.teams
        if data['goods'].teams != teams or data['warehouse'].teams != teams:
            raise serializers.ValidationError

        return data

    def get_goods_name(self, obj):
        return obj.goods.name

    def get_warehouse_name(self, obj):
        return obj.warehouse.name

    def get_completed_quantity(self, obj):
        result = Flow.objects.filter(teams=obj.teams, goods=obj.goods, warehouse=obj.warehouse, create_datetime__gte=obj.start_date,
                                     create_datetime__lte=obj.end_date, sales_order__isnull=False).aggregate(total=Sum('change_quantity'))
        return -result['total'] if result['total'] else 0


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        read_only_fields = ['id']
        fields = ['number', 'name', 'contacts', 'phone', 'email', 'address', 'remark', *read_only_fields]

    def validate(self, data):
        # 编号验证
        teams = self.context['request'].user.teams
        if Client.objects.filter(teams=teams, number=data['number']).exists():
            raise serializers.ValidationError({'number': '编号已存在'})
        return data


class ClientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        read_only_fields = ['id', 'number']
        fields = ['name', 'contacts', 'phone', 'email', 'address', 'remark', *read_only_fields]
