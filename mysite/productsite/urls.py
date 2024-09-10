from django.urls import path, include
from . import views
from productsite.views import product_view
from .views import products_by_category

urlpatterns= [
    path('', views.product_view, name='product_home'), #root url
    path('api/products_by_category/', products_by_category, name='products_by_category'),
]