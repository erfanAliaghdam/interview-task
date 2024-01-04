from django.db import models
from django.db.models import Sum, Prefetch, ExpressionWrapper, F, Count

from shop.models import Cart, CartItem


class CartRepository:
    def add_product_to_cart_by_user_id_and_product_id(
        self, user_id: int, product_id: int
    ):
        cart, _ = Cart.objects.get_or_create(user_id=user_id)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, product_id=product_id
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return cart

    def get_cart_with_all_data_and_total_price_by_user_id(self, user_id: int):
        cart = (
            Cart.objects.filter(user_id=user_id)
            .prefetch_related("items__product")
            .annotate(
                total_price=Sum(
                    F("items__quantity") * F("items__product__price"),
                    default=0,
                    output_field=models.DecimalField(),
                ),
                items_count=Count("items"),
            )
            .first()
        )

        return cart
