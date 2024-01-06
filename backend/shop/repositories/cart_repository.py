from django.db import models
from django.db.models import Sum, F, Count, Case, When, Value

from shop.models import Cart, CartItem


class CartRepository:
    def create_get_or_create_cart_for_user_by_user_id(self, user_id: int):
        return Cart.objects.get_or_create(user_id=user_id)

    def add_product_to_cart_by_user_id_and_product_id(
        self, product_id: int, cart_id: int
    ):
        cart_item, created = CartItem.objects.get_or_create(
            cart_id=cart_id, product_id=product_id
        )
        if not created:
            if not cart_item.quantity < cart_item.product.stock:
                return False
            cart_item.quantity += 1
            cart_item.save()
        return True

    def decrease_product_quantity_from_cart_by_user_id_and_product_id(
        self, product_id: int, user_id: int
    ):
        cart_item = CartItem.objects.filter(
            cart__user_id=user_id, product_id=product_id
        ).first()

        if not cart_item:
            return False
        if cart_item.quantity == 1 or cart_item.quantity == 0:
            cart_item.delete()
        else:
            cart_item.quantity -= 1
            cart_item.save()
        return True

    def get_cart_with_all_data_and_total_price_by_user_id(self, user_id: int):
        cart = (
            Cart.objects.filter(user_id=user_id)
            .prefetch_related("items__product")
            .annotate(
                total_price=Sum(
                    Case(
                        When(
                            items__product__stock__gt=0,
                            then=F("items__quantity") * F("items__product__price"),
                        ),
                        default=Value(0),
                        output_field=models.DecimalField(),
                    ),
                    default=0,
                    output_field=models.DecimalField(),
                ),
                items_count=Count("items"),
                in_stock_items_count=Sum(
                    Case(
                        When(items__product__stock__gt=0, then=1),
                        default=Value(0),
                        output_field=models.IntegerField(),
                    )
                ),
            )
            .first()
        )

        return cart

    def get_cart_items_by_user_id(self, user_id: int):
        return CartItem.objects.select_related("product").filter(cart__user_id=user_id)

    def get_in_stock_cart_items_by_cart_id(self, cart_id: int):
        cart_items = CartItem.objects.select_related("product").filter(
            cart_id=cart_id, product__stock__gt=0
        )
        return cart_items

    def get_out_of_stock_cart_items_by_cart_id(self, cart_id: int):
        cart_items = CartItem.objects.select_related("product").filter(
            cart_id=cart_id, product__stock=0
        )
        return cart_items

    def validate_cart_item_quantity_by_queryset(self, cart_items):
        for cart_item in cart_items:
            if cart_item.quantity > cart_item.product.stock:
                return False
        return True

    def update_cart_items_products_stock_by_queryset(self, cart_items):
        for cart_item in cart_items:
            cart_item.product.stock -= cart_item.quantity
            cart_item.product.save()

        return cart_items
