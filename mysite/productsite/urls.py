from django.urls import path, include
from . import views
from productsite.views import product_view

urlpatterns= [
    path('', views.product_view, name='product_home'), #root url
]