from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('product/grid/',views.ShopProductGridView.as_view(),name='product_grid'),
    path('product/<str:slug>/detail/',views.ShopProductDetailView.as_view(),name='product_detail'),
]
