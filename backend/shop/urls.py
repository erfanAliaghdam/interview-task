from django.urls import path
from shop.api.v1.views import (
    product_list_view,
    product_detail_view,
    user_add_to_cart_view,
    user_cart_list_view,
)

urlpatterns = [
    path("products/", product_list_view, name="products-list"),
    path("products/<slug:slug>/", product_detail_view, name="products-detail"),
    path("cart/", user_cart_list_view, name="cart-list"),
    path("cart/add/<slug:slug>/", user_add_to_cart_view, name="cart-add"),
]
