from django.db import transaction
from django.db.models import F

from core.exceptions import Custom412Exception
from shop.repositories import CartRepository, OrderRepository, ProductRepository


class OrderService:
    def __init__(self, *args, **kwargs):
        self.order_repository = OrderRepository()
        self.cart_repository = CartRepository()
        self.product_repository = ProductRepository()

    @transaction.atomic
    def place_order(
        self,
        user_id: int,
    ):
        cart_items = self.cart_repository.get_cart_items_by_user_id(user_id=user_id)

        # condition1 : if cart is empty
        if not cart_items:
            raise Custom412Exception(detail="your cart is empty.")

        # lock product table
        products = self.product_repository.get_products_by_id_list(
            product_ids=cart_items.values("product_id")
        ).select_for_update()

        cart_item_is_valid = (
            self.cart_repository.validate_cart_item_quantity_by_queryset(
                cart_items=cart_items
            )
        )
        if not cart_item_is_valid:
            raise Custom412Exception(
                "invalid quantity is in your cart, check product stocks."
            )

        # Update product stock using cart_items
        self.cart_repository.update_cart_items_products_stock_by_queryset(
            cart_items=cart_items
        )

        # place order
        order = self.order_repository.create_order(user_id=user_id)
        order_items = (
            self.order_repository.create_order_items_based_on_cart_items_query(
                order_id=order.id, cart_items=cart_items
            )
        )
        cart_items.delete()
        return order_items
