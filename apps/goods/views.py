from utils.permissions import IsAuthenticated, PurchasePricePermission
from .serializers import CategorySerializer, CategoryUpdateSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import GoodsSerializer, GoodsUpdateSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import CategoryPermission, GoodsPermission
from .paginations import CategoryPagination, GoodsPagination
from rest_framework import viewsets


class CategoryViewSet(viewsets.ModelViewSet):
    """商品分类: list, post, retrieve, update, delete"""
    serializer_class = CategorySerializer
    pagination_class = CategoryPagination
    permission_classes = [IsAuthenticated, CategoryPermission]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['number', 'name']
    ordering_fields = ['number', 'name']
    ordering = ['number']

    def get_serializer_class(self):
        return CategoryUpdateSerializer if self.request.method == 'PUT' else self.serializer_class

    def get_queryset(self):
        return self.request.user.teams.categories.all()

    def perform_create(self, serializer):
        serializer.save(teams=self.request.user.teams)


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

    def get_serializer_class(self):
        return GoodsUpdateSerializer if self.request.method == 'PUT' else self.serializer_class

    def get_queryset(self):
        return self.request.user.teams.goods_set.select_related('category').all()

    def perform_create(self, serializer):
        serializer.save(teams=self.request.user.teams)
