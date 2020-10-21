from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('categories/<int:pk>/', views.CategoryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('export/categories/', views.CategoryViewSet.as_view({'get': 'export_excel'})),
    path('import/categories/', views.CategoryViewSet.as_view({'post': 'import_excel'})),
    path('goods/', views.GoodsViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('goods/<int:pk>/', views.GoodsViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('export/goods/', views.GoodsViewSet.as_view({'get': 'export_excel'})),
    path('import/goods/', views.GoodsViewSet.as_view({'post': 'import_excel'})),
]
