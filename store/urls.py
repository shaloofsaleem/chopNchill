# store/urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path('products', ProductPage, name='product_page'),
    path('category/<slug:slug>/', category_products, name='category_detail'),
    path('product/<slug:slug>/',    product_detail, name='product_detail'),
   
]
