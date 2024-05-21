from django.core.exceptions import FieldError
from django.shortcuts import render
from .models import ProductModel,ProductStatusType,ProductCategoryModel
from django.views.generic import ListView,DetailView


class ShopProductGridView(ListView):
    template_name = "shop/product-grid.html"
    context_object_name = 'products'
    paginate_by =6
    
    def get_queryset(self):
        queryset= ProductModel.objects.filter(status=ProductStatusType.publish.value)

        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(title__icontains=search_q)
        if category_id := self.request.GET.get("category_id"):
            queryset = queryset.filter(category__id=category_id)
        if min_price := self.request.GET.get("min_price"):
            queryset = queryset.filter(price__gte=min_price)
        if max_price := self.request.GET.get("max_price"):
            queryset = queryset.filter(price__lte=max_price)
        if order_by := self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['total_items']=self.get_queryset().count()
        context["categories"] = ProductCategoryModel.objects.all()
        return context
        
        
class ShopProductDetailView(DetailView):
    template_name="shop/product-detail.html"
    context_object_name = 'product'
    
    def get_queryset(self):
        return ProductModel.objects.filter(status=ProductStatusType.publish.value)
        
        