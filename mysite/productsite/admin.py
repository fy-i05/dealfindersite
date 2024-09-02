from django.contrib import admin
from .models import Products, Category
# Register your models here.

admin.site.register(Products)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',) #search box for searching items