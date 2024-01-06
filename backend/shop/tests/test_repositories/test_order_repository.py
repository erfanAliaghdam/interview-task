from datetime import datetime, timedelta
from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.test import TestCase
from model_bakery import baker
from shop.models import Order, Cart, CartItem, OrderItem
from shop.repositories import OrderRepository


class OrderRepositoryTest(TestCase):
    def setUp(self) -> None:
        self.user = baker.make(get_user_model())
        self.order = baker.make(Order, user=self.user)
        self.repository = OrderRepository()

    def test_create_order(self):
        self.assertEqual(Order.objects.filter(user_id=self.user.id).count(), 1)
        order = self.repository.create_order(user_id=self.user.id)
        self.assertEqual(order.user.id, self.user.id)
        self.assertEqual(Order.objects.filter(user_id=self.user.id).count(), 2)

    @patch(
        "shop.repositories.order_repository.CartRepository.get_cart_items_by_user_id"
    )
    def test_create_order_items_based_on_cart_items(
        self, get_cart_items_by_user_id_mock
    ):
        self.assertEqual(
            OrderItem.objects.filter(order__user_id=self.user.id).count(), 0
        )

        cart = Cart.objects.filter(user_id=self.user.id).first()
        cart_items = baker.make(CartItem, cart=cart, _quantity=3)

        get_cart_items_by_user_id_mock.return_value = CartItem.objects.filter(
            cart__user_id=self.user.id
        )
        result = self.repository.create_order_items_based_on_cart_items_query(
            order_id=self.order.id, cart_items=cart_items
        )
        user_order_items = OrderItem.objects.filter(order__user_id=self.user.id)
        self.assertEqual(user_order_items.count(), 3)
        self.assertEqual(len(result), user_order_items.count())
        for item in result:
            self.assertTrue(OrderItem.objects.filter(id=item.id).exists())

    def test_get_order_count_by_created_at_range(self):
        orders = baker.make(Order, status=Order.CHECKED, _quantity=3)
        orders[0].created_at = datetime.now() - timedelta(days=2)
        orders[0].save()
        start = datetime.now() - timedelta(days=1)
        finish = datetime.now()
        orders_count = self.repository.get_checked_order_count_by_created_at_range(
            start=start, finish=finish
        )
        self.assertEqual(orders_count, 2)
        start = datetime.now() - timedelta(days=3)
        orders_count = self.repository.get_checked_order_count_by_created_at_range(
            start=start, finish=finish
        )
        self.assertEqual(orders_count, 3)

    def test_get_order_with_all_data_and_total_price_by_user_id(self):
        orders = Order.objects.filter(user=self.user).prefetch_related("items")
        orders_count = orders.count()
        order_total_price = sum(
            item.price * item.quantity for item in orders.first().items.all()
        )
        result = self.repository.get_order_with_all_data_and_total_price_by_user_id(
            user_id=self.user.id
        )
        self.assertEqual(orders_count, result.count())
        self.assertEqual(orders.first().items.all().count(), result[0].items_count)
        self.assertEqual(order_total_price, result[0].total_price)
