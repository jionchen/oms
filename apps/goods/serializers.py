from .validations import goods_validate
from rest_framework import serializers
from .models import Category, Goods


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        read_only_fields = ['id']
        fields = ['number', 'name', 'remark', *read_only_fields]

    def validate(self, data):
        # 编号验证
        teams = self.context['request'].user.teams
        if Category.objects.filter(teams=teams, number=data['number']).exists():
            raise serializers.ValidationError({'number': '编号已存在'})
        return data


class CategoryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        read_only_fields = ['id', 'number']
        fields = ['name', 'remark', *read_only_fields]


class GoodsSerializer(serializers.ModelSerializer):
    category_number = serializers.SerializerMethodField('get_category_number')
    category_name = serializers.SerializerMethodField('get_category_name')

    class Meta:
        model = Goods
        read_only_fields = ['id', 'category_number', 'category_name']
        fields = ['number', 'name', 'unit', 'category', 'purchase_price', 'retail_price',
                  'shelf_life_warnning', 'shelf_life', 'shelf_life_warnning_days', 'inventory_upper',
                  'inventory_lower', 'inventory_warning', 'remark', 'is_active', *read_only_fields]

    def validate(self, data):
        # 编号验证
        teams = self.context['request'].user.teams
        if Goods.objects.filter(teams=teams, number=data['number']).exists():
            raise serializers.ValidationError({'number': '编号已存在'})

        goods_validate(self.context['request'], data)
        return data

    def get_category_number(self, obj):
        return obj.category.number if obj.category else None

    def get_category_name(self, obj):
        return obj.category.name if obj.category else None


class GoodsUpdateSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField('get_category_name')

    class Meta:
        model = Goods
        read_only_fields = ['id', 'number', 'category_name']
        fields = ['name', 'unit', 'category', 'purchase_price', 'retail_price', 'shelf_life_warnning',
                  'shelf_life', 'shelf_life_warnning_days', 'inventory_upper', 'inventory_lower',
                  'inventory_warning', 'remark', 'is_active', *read_only_fields]

    def validate(self, data):
        goods_validate(self.context['request'], data)
        return data

    def get_category_name(self, obj):
        return obj.category.name if obj.category else None
