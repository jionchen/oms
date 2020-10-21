from .filters import PurcahseReportFilter, SalesReportFilter, ProfitTrendFilter, PurchaseStatisticsFilter, SalesStatisticsFilter
from .paginations import PurchaseReportPagination, SalesReportPagination
from utils.permissions import IsAuthenticated, PurchasePricePermission
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count, Avg, Max, Min, F
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from apps.warehouse.models import Flow, Warehouse
from apps.purchase.models import PurchaseGoods, PurchaseOrder, PaymentRecord as PurchasePaymentRecord
from rest_framework import viewsets
from apps.sales.models import SalesGoods, SalesOrder, PaymentRecord as SalesPaymentRecord
from rest_framework.filters import SearchFilter
import pendulum
from rest_framework.exceptions import ValidationError


class PurcahseReportViewSet(viewsets.ModelViewSet):
    """采购报表: list"""
    permission_classes = [IsAuthenticated, PurchasePricePermission]
    filter_backends = [DjangoFilterBackend]
    pagination_class = PurchaseReportPagination
    filterset_class = PurcahseReportFilter

    def get_queryset(self):
        return PurchaseGoods.objects.filter(purchase_order__teams=self.request.user.teams, purchase_order__is_return=False)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        report_type = request.GET.get('type')

        if report_type == 'goods':
            results = queryset.values('goods').annotate(quantity=Sum('quantity'), min_purchase_price=Min('discount_price'),
                                                        max_purchase_price=Max('discount_price'),
                                                        avg_purchase_price=Avg('discount_price'))
            results = results.values('quantity', 'min_purchase_price', 'max_purchase_price', 'avg_purchase_price',
                                     code=F('goods__code'), name=F('goods__name'), specification=F('goods__specification'),
                                     unit=F('goods__unit')).order_by('code')
        else:
            results = queryset.values('code', 'name', 'specification', 'unit', 'quantity',
                                      date=F('purchase_order__date'), category_name=F('goods__category__name'),
                                      supplier_name=F('purchase_order__supplier_name'),
                                      warehouse_name=F('purchase_order__warehouse_name'),
                                      relation_order=F('purchase_order')).order_by('-purchase_order__date')

        total = queryset.aggregate(times=Count('purchase_order'), quantity=Sum('quantity'), amount=Sum('discount_amount'))
        return Response({'total': total, 'results': self.paginate_queryset(results)})


class SalesReportViewSet(viewsets.ModelViewSet):
    """销售报表: list"""
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    pagination_class = SalesReportPagination
    filterset_class = SalesReportFilter

    def get_queryset(self):
        return SalesGoods.objects.filter(sales_order__teams=self.request.user.teams, sales_order__is_return=False)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        report_type = request.GET.get('type')

        if report_type == 'goods':
            results = queryset.values('goods').annotate(quantity=Sum('quantity'), min_retail_price=Min('retail_price'),
                                                        max_retail_price=Max('retail_price'),
                                                        avg_retail_price=Avg('retail_price'))
            results = results.values('quantity', 'min_retail_price', 'max_retail_price', 'avg_retail_price',
                                     code=F('goods__code'), name=F('goods__name'), specification=F('goods__specification'),
                                     unit=F('goods__unit')).order_by('code')
        else:
            results = queryset.values('code', 'name', 'specification', 'unit', 'quantity',
                                      date=F('sales_order__date'), category_name=F('goods__category__name'),
                                      seller_name=F('sales_order__seller_name'),
                                      warehouse_name=F('sales_order__warehouse_name'),
                                      relation_order=F('sales_order')).order_by('-sales_order__date')

        total = queryset.aggregate(cost=Sum(F('quantity') * F('purchase_price')), quantity=Sum('quantity'),
                                   amount=Sum(F('quantity') * F('retail_price') * F('sales_order__discount') * 0.01))
        return Response({'total': total, 'results': self.paginate_queryset(results)})


class SalesTrendViewSet(viewsets.ModelViewSet):
    """销售趋势"""
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        if not start_date or not end_date:
            raise ValidationError
        end_date = pendulum.parse(end_date).add(days=1)

        queryset = SalesOrder.objects.filter(teams=request.user.teams, is_return=False)
        queryset = queryset.filter(date__gte=start_date, date__lte=end_date)
        queryset = queryset.extra(select={'_date': 'DATE_FORMAT(date, "%%Y-%%m-%%d")'})
        queryset = queryset.values('_date', _warehouse=F('warehouse__name'))
        results = queryset.annotate(_amount=Sum('total_amount'))

        warehouse_list = Warehouse.objects.filter(
            teams=request.user.teams, is_delete=False).values_list('name', flat=True)
        return Response({'results': results, 'warehouse_list': warehouse_list})


class ProfitTrendViewSet(viewsets.ModelViewSet):
    """利润趋势"""
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProfitTrendFilter

    def get_queryset(self):
        return SalesGoods.objects.filter(sales_order__teams=self.request.user.teams, sales_order__is_return=False)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.extra(select={'_date': 'DATE_FORMAT(`sales_salesorder`.`date`, "%%Y-%%m-%%d")'})
        queryset = queryset.values('_date', _warehouse=F('sales_order__warehouse__name'))
        results = queryset.annotate(
            _amount=Sum((F('retail_price') * F('sales_order__discount') * 0.01 - F('purchase_price')) * F('quantity')))

        warehouse_list = Warehouse.objects.filter(
            teams=request.user.teams, is_delete=False).values_list('name', flat=True)
        return Response({'results': results, 'warehouse_list': warehouse_list})


# class FinancialReportViewSet(viewsets.ModelViewSet):
#     """财务报表: list"""
#     permission_classes = [IsAuthenticated]
#     filter_backends = [DjangoFilterBackend]
#     filterset_class = FinancialReportFilter

#     def get_queryset(self):
#         return SalesGoods.objects.filter(sales_order__teams=self.request.user.teams, sales_order__is_return=False)

#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())
#         queryset = queryset.extra(select={'_date': 'DATE_FORMAT(`sales_salesorder`.`date`, "%%Y-%%m-%%d")'})
#         queryset = queryset.values('_date', _warehouse=F('sales_order__warehouse__name'))
#         results = queryset.annotate(
#             _amount=Sum((F('retail_price') * F('sales_order__discount') * 0.01 - F('purchase_price')) * F('quantity')))

#         warehouse_list = Warehouse.objects.filter(
#             teams=request.user.teams, is_delete=False).values_list('name', flat=True)
#         return Response({'results': results, 'warehouse_list': warehouse_list})


class FinancialStatisticsViewSet(viewsets.ModelViewSet):
    """财务统计: list"""
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        teams = request.user.teams
        sales_amount = SalesPaymentRecord.objects.filter(
            sales_order__teams=teams, sales_order__is_return=False
        ).aggregate(amount=Sum('amount'))['amount']
        sales_return_amount = SalesPaymentRecord.objects.filter(
            sales_order__teams=teams, sales_order__is_return=True
        ).aggregate(amount=Sum('amount'))['amount']
        purchase_amount = PurchasePaymentRecord.objects.filter(
            purchase_order__teams=teams, purchase_order__is_return=False
        ).aggregate(amount=Sum('amount'))['amount']
        purchase_return_amount = PurchasePaymentRecord.objects.filter(
            purchase_order__teams=teams, purchase_order__is_return=True
        ).aggregate(amount=Sum('amount'))['amount']

        sales_amount = sales_amount if sales_amount else 0
        sales_return_amount = sales_return_amount if sales_return_amount else 0
        purchase_amount = purchase_amount if purchase_amount else 0
        purchase_return_amount = purchase_return_amount if purchase_return_amount else 0

        return Response({'sales_amount': sales_amount, 'sales_return_amount': sales_return_amount,
                         'purchase_amount': purchase_amount, 'purchase_return_amount': purchase_return_amount})


class PurchaseStatisticsViewSet(viewsets.ModelViewSet):
    """采购统计: list"""
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_class = PurchaseStatisticsFilter
    search_fields = ['id']

    def get_queryset(self):
        return self.request.user.teams.purchase_order_set.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        results = queryset.filter(is_return=False).aggregate(total_amount=Sum('total_amount'),
                                                             amount=Sum('amount'))
        total_amount = results['total_amount']
        total_amount = total_amount if total_amount else 0
        amount = results['amount']
        amount = amount if amount else 0
        return_amount = queryset.filter(is_return=True).aggregate(amount=Sum('amount'))['amount']
        return_amount = return_amount if return_amount else 0

        return Response({'total_amount': total_amount, 'amount': amount, 'return_amount': return_amount})


class SalesStatisticsViewSet(viewsets.ModelViewSet):
    """销售统计: list"""
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_class = SalesStatisticsFilter
    search_fields = ['id']

    def get_queryset(self):
        return self.request.user.teams.sales_order_set.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        results = queryset.filter(is_return=False).aggregate(total_amount=Sum('total_amount'),
                                                             amount=Sum('amount'))
        total_amount = results['total_amount']
        total_amount = total_amount if total_amount else 0
        amount = results['amount']
        amount = amount if amount else 0
        return_amount = queryset.filter(is_return=True).aggregate(amount=Sum('amount'))['amount']
        return_amount = return_amount if return_amount else 0

        return Response({'total_amount': total_amount, 'amount': amount, 'return_amount': return_amount})
