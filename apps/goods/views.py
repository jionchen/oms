from rest_framework.exceptions import ValidationError
from apps.goods.models import Category, Goods
from utils.permissions import IsAuthenticated, PurchasePricePermission
from .serializers import CategorySerializer, CategoryUpdateSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import GoodsSerializer, GoodsUpdateSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import CategoryPermission, GoodsPermission
from .paginations import CategoryPagination, GoodsPagination
from rest_framework import viewsets
from utils.excel import export_excel, import_excel
from rest_framework.decorators import action
from django.db import transaction
from rest_framework.status import HTTP_201_CREATED
from rest_framework.response import Response
from apps.purchase.models import ChangeRecord


class CategoryViewSet(viewsets.ModelViewSet):
    """商品分类: list, post, retrieve, update, delete"""
    serializer_class = CategorySerializer
    pagination_class = CategoryPagination
    permission_classes = [IsAuthenticated, CategoryPermission]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['number', 'name']
    ordering_fields = ['number', 'name']
    ordering = ['number']
    field_mapping = (('number', '编号'), ('name', '名称'), ('remark', '备注'))

    def get_serializer_class(self):
        return CategoryUpdateSerializer if self.request.method == 'PUT' else self.serializer_class

    def get_queryset(self):
        return self.request.user.teams.categories.all()

    def perform_create(self, serializer):
        serializer.save(teams=self.request.user.teams)

    @action(detail=False)
    def export_excel(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return export_excel(serializer.data, '分类列表', self.field_mapping)

    @action(detail=False)
    @transaction.atomic
    def import_excel(self, request, *args, **kwargs):
        Category.objects.bulk_create([Category(**item, teams=request.user.teams)
                                      for item in import_excel(self, self.field_mapping)])
        return Response(status=HTTP_201_CREATED)


class GoodsViewSet(viewsets.ModelViewSet):
    """商品:　list, post, retrieve, update, delete"""
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    permission_classes = [IsAuthenticated, GoodsPermission, PurchasePricePermission]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filter_fields = ['category', 'is_active']
    search_fields = ['number', 'name']
    ordering_fields = ['number', 'name', 'purchase_price', 'retail_price']
    ordering = ['number']
    field_mapping = (('number', '编号'), ('name', '名称'), ('unit', '单位'), ('category_number', '分类编号'),
                     ('purchase_price', '采购价'), ('retail_price', '零售价'), ('shelf_life', '保质期'),
                     ('shelf_life_warnning_days', '保质期预警天数'), ('inventory_upper', '库存上限'),
                     ('inventory_lower', '库存下线'), ('inventory_warning', '库存预警'), ('is_active', '状态'))

    def get_serializer_class(self):
        return GoodsUpdateSerializer if self.request.method == 'PUT' else self.serializer_class

    def get_queryset(self):
        return self.request.user.teams.goods_set.select_related('category').all()

    def perform_create(self, serializer):
        serializer.save(teams=self.request.user.teams)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        # 采购价变更记录
        purchase_price = request.data.get('purchase_price', 0)
        if purchase_price != instance.purchase_price:
            ChangeRecord.objects.create(goods=instance, goods_number=instance.number,
                                        goods_name=instance.name, unit=instance.unit,
                                        before_change=instance.purchase_price,
                                        after_change=purchase_price, operator=request.user,
                                        operator_name=request.user.name,
                                        teams=request.user.teams)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @action(detail=False)
    def export_excel(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return export_excel(serializer.data, '商品列表', self.field_mapping)

    @action(detail=False)
    @transaction.atomic
    def import_excel(self, request, *args, **kwargs):
        Goods.objects.bulk_create(self.import_validate(import_excel(self, self.field_mapping)))
        return Response(status=HTTP_201_CREATED)

    def import_validate(self, data):
        teams = self.request.user.teams
        for item in data:
            category_number = item.pop('category_number')
            category = Category.objects.filter(teams=teams, number=category_number).first()
            if not category:
                raise ValidationError({'message': '分类不存在'})

            item['category'] = category
            item['teams'] = teams
            yield Goods(**item)
