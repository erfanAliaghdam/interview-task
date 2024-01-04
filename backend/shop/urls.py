from django.urls import path
from shop.api.v1.views import product_list_view, product_detail_view

urlpatterns = [
    path("products/", product_list_view, name="products-list"),
    path("products/<slug:slug>/", product_detail_view, name="products-detail"),
]
