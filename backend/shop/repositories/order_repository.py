from django.db import models
from django.db.models import Sum, Case, When, F, Value, Count
from shop.models import Order, OrderItem
from shop.repositories import CartRepository

cart_repository = CartRepository()


class OrderRepository:
    def create_order(self, user_id: int):
        return Order.objects.create(user_id=user_id)

    def create_order_items_based_on_cart_items_query(self, order_id: int, cart_items):
        order_items = []
        for cart_item in cart_items:
            order_items.append(
                OrderItem(
                    order_id=order_id,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price,
                )
            )
        order_items = OrderItem.objects.bulk_create(order_items)
        return order_items

    def get_checked_order_count_by_created_at_range(self, start, finish):
        return Order.objects.filter(
            status=Order.CHECKED, created_at__range=(start, finish)
        ).count()

    def get_order_with_all_data_and_total_price_by_user_id(self, user_id: int):
        orders = (
            Order.objects.filter(user_id=user_id)
            .prefetch_related("items__product")
            .annotate(
                items_count=Count("items"),
                total_price=Sum(
                    F("items__quantity") * F("items__price"),
                    default=0,
                    output_field=models.DecimalField(max_digits=12, decimal_places=2),
                ),
            )
        )
        return orders
