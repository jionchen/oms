from rest_framework.serializers import ValidationError
from apps.goods.models import Category


def goods_validate(request, data):
    if data.get('purchase_price', 0) < 0:
        raise ValidationError({'purchase_price': '采购价不能小于0'})

    if data.get('retail_price', 0) < 0:
        raise ValidationError({'retail_price': '零售价不能小于0'})

    if data.get('shelf_life') is not None and data['shelf_life'] < 0:
        raise ValidationError({'shelf_life': '保质期不能小于0'})

    if data.get('shelf_life_warnning_days') is not None and data['shelf_life_warnning_days'] < 0:
        raise ValidationError({'shelf_life_warnning_days': '预警天数不能小于0'})

    if data.get('shelf_life_warnning_days', 0) > data.get('shelf_life', 0):
        raise ValidationError({'shelf_life_warnning_days': '预警天数不能大于保质期'})

    if data.get('inventory_lower') is not None and data['inventory_lower'] < 0:
        raise ValidationError({'inventory_lower': '库存下限不能小于0'})

    if data.get('inventory_upper') is not None and data['inventory_upper'] < 0:
        raise ValidationError({'inventory_upper': '库存上限不能小于0'})

    if data.get('inventory_lower', 0) > data.get('inventory_upper', 0):
        raise ValidationError({'inventory_upper': '库存上限不能小于库存下限'})

    # 商品分类验证
    category = data.get('category')
    if category is not None and not Category.objects.filter(teams=request.user.teams, id=category.id).exists():
        raise ValidationError({'category': '商品分类不存在'})
