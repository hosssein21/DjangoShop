from typing import Any
from django.shortcuts import render
from .models import ProductModel,ProductStatusType
from django.views.generic import ListView,TemplateView


class ShopProductGridView(ListView):
    template_name = "shop/product-grid.html"
    context_object_name = 'products'
    
    def get_queryset(self):
        return ProductModel.objects.filter(status=ProductStatusType.publish.value)
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['total_items']=self.get_queryset().count()
        return context
        
        
        