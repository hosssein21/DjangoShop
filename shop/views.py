from django.shortcuts import render
from .models import ProductModel,ProductStatusType
from django.views.generic import ListView,TemplateView


class ShopProductGridView(TemplateView):
    template_name = "shop/product-grid.html"
    # queryset=ProductModel.objects.filter(ProductStatusType.publish.value)
