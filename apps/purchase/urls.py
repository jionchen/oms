from django.urls import path
from . import views

urlpatterns = [
    path('suppliers/', views.SupplierViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('suppliers/<int:pk>/', views.SupplierViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('export/suppliers/', views.SupplierViewSet.as_view({'get': 'export_excel'})),
    path('import/suppliers/', views.SupplierViewSet.as_view({'post': 'import_excel'})),
    path('purchase_order/confirm/', views.PurchaseOrderViewSet.as_view({'post': 'confirm'})),
    path('purchase_order/payment/', views.PurchaseOrderViewSet.as_view({'post': 'payment'})),
    path('purchase_order/', views.PurchaseOrderViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('purchase_order/<str:pk>/', views.PurchaseOrderViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),
    path('purchase_price_records/', views.PurchasePriceRecordViewSet.as_view({'get': 'list'})),
    path('purchase_payment_records/', views.PurchasePaymentRecordViewSet.as_view({'get': 'list'})),
]
