from django.contrib import admin
from .models import Products, Category


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'original_price', 'current_price', 'get_deal_rating')
    search_fields = ('name', 'category__name') 

admin.site.register(Products, ProductAdmin)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'parent')
    search_fields = ('name',)
