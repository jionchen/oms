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
        read_only_fields = ['id', 'number', 'supplier_name', 'warehouse_name', 'warehouse_address', 'account_name',
                            'contacts_name', 'contacts_phone', 'is_commit', 'goods_set', 'total_amount']
        fields = ['supplier', 'warehouse', 'account', 'contacts', 'amount', 'date', 'remark',
                  *read_only_fields]

    def validate(self, data):
        if len(self.context['request'].data.get('goods_set', [])) == 0:
            raise serializers.ValidationError('表单商品不能为空')
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
