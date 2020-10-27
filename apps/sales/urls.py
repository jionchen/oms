from django.urls import path
from . import views

urlpatterns = [
    # path('sales_orders/confirm/', views.SalesOrderViewSet.as_view({'post': 'confirm'})),
    # path('sales_orders/payment/', views.SalesOrderViewSet.as_view({'post': 'payment'})),
    path('sales_orders/', views.SalesOrderViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('sales_orders/<int:pk>/', views.SalesOrderViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),
    path('sales_orders/<int:pk>/commit/', views.SalesOrderViewSet.as_view({'post': 'commit'})),

    path('sales_tasks/', views.SalesTaskViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('sales_order_profit/total_profit/', views.SalesOrderProfitViewSet.as_view({'get': 'total_profit'})),
    path('sales_order_profit/', views.SalesOrderProfitViewSet.as_view({'get': 'list'})),
    path('sales_order_profit/<int:pk>/', views.SalesOrderProfitViewSet.as_view({'put': 'update'})),
    path('clients/', views.ClientViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('clients/<int:pk>/', views.ClientViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('export/clients/', views.ClientViewSet.as_view({'get': 'export_excel'})),
    path('import/clients/', views.ClientViewSet.as_view({'post': 'import_excel'})),
    path('sales_payment_records/', views.SalesPaymentRecordViewSet.as_view({'get': 'list'})),
]
