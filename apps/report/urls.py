from django.urls import path
from . import views

urlpatterns = [
    path('purchase_reports/', views.PurcahseReportViewSet.as_view({'get': 'list'})),
    path('sales_reports/', views.SalesReportViewSet.as_view({'get': 'list'})),
    path('financial_statistics/', views.FinancialStatisticsViewSet.as_view({'get': 'list'})),
    path('purchase_statistics/', views.PurchaseStatisticsViewSet.as_view({'get': 'list'})),
    path('sales_statistics/', views.SalesStatisticsViewSet.as_view({'get': 'list'})),
    path('sales_trends/', views.SalesTrendViewSet.as_view({'get': 'list'})),
    path('profit_trends/', views.ProfitTrendViewSet.as_view({'get': 'list'})),
]
