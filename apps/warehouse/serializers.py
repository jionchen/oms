from .models import Warehouse, Inventory, Flow, CountingList, Requisition
from goods.serializers import GoodsSerializer
from rest_framework import serializers
from django.db.models import Sum, F
from goods.models import Goods
from user.models import User


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        read_only_fields = ['id', 'create_date', 'update_date']
        fields = ['number', 'name', 'manager', 'address', 'remark', 'is_active', *read_only_fields]

    def validate(self, data):
        teams = self.context['request'].user.teams

        # 编号验证
        if Warehouse.objects.filter(teams=teams, number=data['number']).exists():
            raise serializers.ValidationError({'number': '编号已存在'})

        # 负责人验证
        manager = data.get('manager')
        if manager is not None and not User.objects.filter(teams=teams, username=manager.username).exists():
            raise serializers.ValidationError({'category': '账户不存在'})

        return data


class WarehouseUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        read_only_fields = ['id', 'number', 'create_date', 'update_date']
        fields = ['name', 'manager', 'address', 'remark', 'is_active', *read_only_fields]

    def validate(self, data):
        # 负责人验证
        teams = self.context['request'].user.teams
        manager = data.get('manager')
        if manager is not None and not User.objects.filter(teams=teams, username=manager.username).exists():
            raise serializers.ValidationError({'category': '账户不存在'})
        return data


class InventorySerializer(serializers.ModelSerializer):
    goods = serializers.SerializerMethodField('get_goods')
    warehouse_name = serializers.SerializerMethodField('get_warehouse_name')
    total = serializers.SerializerMethodField('get_total')

    class Meta:
        model = Inventory
        fields = ['goods', 'quantity', 'warehouse_name', 'total']
        read_only_fields = fields

    def get_goods(self, obj):
        return {
            'code': obj.goods.code,
            'name': obj.goods.name,
            'brand': obj.goods.brand,
            'specification': obj.goods.specification,
            'unit': obj.goods.unit,
            'category_name': obj.goods.category.name if obj.goods.category else '',
            'purchase_price': obj.goods.purchase_price,
        }

    def get_warehouse_name(self, obj):
        return obj.warehouse.name

    def get_total(self, obj):
        return self.context['request'].user.teams.inventory_set.all().aggregate(
            quantity=Sum('quantity'), amount=Sum(F('quantity') * F('goods__purchase_price')))


class FlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flow
        fields = ['create_datetime', 'goods_code', 'goods_name', 'specification', 'unit',
                  'warehouse_name', 'type', 'change_quantity', 'remain_quantity', 'operator',
                  'requisition', 'counting_list', 'purchase_order', 'sales_order']
        read_only_fields = fields


class CountingListSerializer(serializers.ModelSerializer):
    goods_set = serializers.SerializerMethodField('get_goods_set')

    class Meta:
        model = CountingList
        read_only_fields = ['id', 'warehouse_name', 'goods_set', 'date']
        fields = ['warehouse', 'remark', *read_only_fields]

    def validate(self, data):
        if not data.get('warehouse'):
            raise serializers.ValidationError

        # goods_set
        goods_set = self.context['request'].data.get('goods_set', [])
        if not goods_set:
            raise serializers.ValidationError

        for item in goods_set:
            if item.get('id') is None or not item.get('quantity') or item['quantity'] <= 0:
                raise serializers.ValidationError

        return data

    def get_goods_set(self, obj):
        return obj.goods_set.all().values('id', 'code', 'name', 'specification', 'unit', 'quantity',
                                          'before_counting', 'purchase_price')


class RequisitionSerializer(serializers.ModelSerializer):
    goods_set = serializers.SerializerMethodField('get_goods_set')

    class Meta:
        model = Requisition
        read_only_fields = ['id', 'out_warehouse_name', 'into_warehouse_name', 'goods_set']
        fields = ['out_warehouse', 'into_warehouse', 'date', 'remark', *read_only_fields]

    def validate(self, data):
        if not data.get('out_warehouse') or not data.get('into_warehouse') or not data.get('date'):
            raise serializers.ValidationError

        # goods_set
        goods_set = self.context['request'].data.get('goods_set', [])
        if not goods_set:
            raise serializers.ValidationError

        for item in goods_set:
            if item.get('id') is None or not item.get('quantity') or item['quantity'] <= 0:
                raise serializers.ValidationError

        return data

    def get_goods_set(self, obj):
        return obj.goods_set.all().values('id', 'code', 'name', 'specification', 'unit', 'quantity')
