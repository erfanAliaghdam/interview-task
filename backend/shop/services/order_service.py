from shop.models import Order, OrderItem
from shop.repositories import CartRepository, OrderRepository


class OrderService:
    def __init__(self, *args, **kwargs):
        self.order_repository = OrderRepository()

    def place_order(
        self,
        user_id: int
    ):
        order = self.order_repository.create_order(user_id=user_id)
        order_items = self.order_repository.create_order_items_based_on_cart_items(
            user_id=user_id,
            order_id=order.id
        )
        return order_items
