from django.contrib import admin

from django.contrib import admin
from .models import ProductModel, ProductImageModel, ProductCategoryModel

# Register your models here.

@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "stock", "status","price", "created_date")
    list_display_links = ['id','title']
    list_filter=['status']
    
@admin.register(ProductCategoryModel)
class ProductCategoryModelAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_date")

@admin.register(ProductImageModel)
class ProductImageModelAdmin(admin.ModelAdmin):
    list_display = ("id", "file", "created_date")
    
    