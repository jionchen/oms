"""oms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import ccccc, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path, include
from . import views


urlpatterns = [
    re_path('user/', include('apps.user.urls')),

    path('api/', include('apps.account.urls')),
    path('api/', include('apps.goods.urls')),
    path('api/', include('apps.warehouse.urls')),
    path('api/', include('apps.purchase.urls')),
    path('api/', include('apps.sales.urls')),
    path('api/', include('apps.report.urls')),

    re_path('^.*$', views.index),
]
