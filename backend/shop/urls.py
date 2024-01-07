from django.urls import path
from shop.api.v1.views import (
    product_list_view,
    product_detail_view,
    user_add_to_cart_view,
    user_cart_list_view,
    user_make_order_view,
    user_order_list_view,
    user_decrease_cart_quantity_view,
    product_create_view,
)

urlpatterns = [
    path("products/", product_list_view, name="products-list"),
    path("products/<slug:slug>/", product_detail_view, name="products-detail"),
    path("sale/products/create/", product_create_view, name="sale-products-create"),
    path("client/cart/", user_cart_list_view, name="client-cart-list"),
    path("client/cart/add/<slug:slug>/", user_add_to_cart_view, name="client-cart-add"),
    path(
        "client/cart/quantity/decrease/<slug:slug>/",
        user_decrease_cart_quantity_view,
        name="client-cart-decrease",
    ),
    path("client/cart/order/", user_make_order_view, name="client-cart-order"),
    path("client/orders/", user_order_list_view, name="client-orders-list"),
]
