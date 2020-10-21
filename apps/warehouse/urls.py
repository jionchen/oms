from django.urls import path
from . import views

urlpatterns = [
    path('warehouses/', views.WarehouseViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('warehouses/<int:pk>/', views.WarehouseViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('export/warehouses/', views.WarehouseViewSet.as_view({'get': 'export_excel'})),
    path('import/warehouses/', views.WarehouseViewSet.as_view({'post': 'import_excel'})),
    path('inventory/', views.InventoryViewSet.as_view({'get': 'list'})),
    path('inventory/export/', views.InventoryViewSet.as_view({'get': 'export'})),
    path('flows/', views.FlowViewSet.as_view({'get': 'list'})),
    path('counting_list/', views.CountingListViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('counting_list/<str:pk>/', views.CountingListViewSet.as_view({'get': 'retrieve'})),
    path('requisition/', views.RequisitionViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('requisition/<str:pk>/', views.RequisitionViewSet.as_view({'get': 'retrieve'})),
]
