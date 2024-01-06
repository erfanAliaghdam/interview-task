from django.db import models
from django.db.models import Sum, Prefetch, ExpressionWrapper, F, Count

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
