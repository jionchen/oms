from .models import Supplier, PurchaseOrder, PurchasePriceRecord, PaymentRecord
from rest_framework import serializers


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        read_only_fields = ['id']
        fields = ['number', 'name', 'contacts', 'phone', 'email', 'address', 'remark', *read_only_fields]

    def validate(self, data):
        # 编号验证
        teams = self.context['request'].user.teams
        if Supplier.objects.filter(teams=teams, number=data['number']).exists():
            raise serializers.ValidationError({'number': '编号已存在'})
        return data


class SupplierUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        read_only_fields = ['id', 'number']
        fields = ['name', 'contacts', 'phone', 'email', 'address', 'remark', *read_only_fields]


class PurchaseOrderSerializer(serializers.ModelSerializer):
    goods_set = serializers.SerializerMethodField('get_goods_set')

    class Meta:
        model = PurchaseOrder
        read_only_fields = ['id', 'supplier_name', 'warehouse_name', 'warehouse_address', 'account_name',
                            'contacts_name', 'contacts_phone', 'is_commit', 'goods_set', 'total_amount']
        fields = ['supplier', 'warehouse', 'account', 'contacts', 'amount', 'date', 'remark',
                  'purchase_order', *read_only_fields]

    def validate(self, data):
        if not data.get('supplier') or not data.get('warehouse') or not data.get('account'):
            raise serializers.ValidationError

        if not data.get('contacts') or data.get('amount') is None or not data.get('date'):
            raise serializers.ValidationError

        # goods_set
        goods_set = self.context['request'].data.get('goods_set', [])
        if not goods_set:
            raise serializers.ValidationError

        for item in goods_set:
            if item.get('id') is None or item.get('purchase_price') is None:
                raise serializers.ValidationError

            quantity = item.get('quantity')
            discount = item.get('discount')
            if not quantity or quantity <= 0 or not discount or discount <= 0:
                raise serializers.ValidationError

        # 退货单
        if data.get('is_return', False) and not data.get('purchase_order'):
            raise serializers.ValidationError

        return data

    def get_goods_set(self, obj):
        return obj.goods_set.all().values('id', 'number', 'name', 'unit', 'purchase_price', 'quantity',
                                          'discount', 'discount_price', 'amount', 'discount_amount')


class PurchasePaymentRecordSerializer(serializers.ModelSerializer):
    supplier_name = serializers.SerializerMethodField('get_supplier_name')

    class Meta:
        model = PaymentRecord
        read_only_fields = ['purchase_order', 'date', 'amount',  'remark', 'supplier_name']
        fields = [*read_only_fields]

    def get_supplier_name(self, obj):
        return obj.purchase_order.supplier_name


class PurchasePriceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchasePriceRecord
        read_only_fields = ['create_datetime', 'goods_number', 'goods_name', 'before_change',
                            'after_change', 'operator', 'operator_name']
        fields = [*read_only_fields]
