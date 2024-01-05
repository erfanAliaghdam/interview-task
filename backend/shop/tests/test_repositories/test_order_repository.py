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

    @patch("shop.repositories.order_repository.CartRepository.get_cart_items_by_user_id")
    def test_create_order_items_based_on_cart_items(self, get_cart_items_by_user_id_mock):
        self.assertEqual(OrderItem.objects.filter(order__user_id=self.user.id).count(), 0)

        cart = baker.make(Cart, user=self.user)
        baker.make(CartItem, cart=cart, _quantity=3)

        get_cart_items_by_user_id_mock.return_value = CartItem.objects.filter(cart__user_id=self.user.id)
        result = self.repository.create_order_items_based_on_cart_items(
            user_id=self.user.id,
            order_id=self.order.id
        )
        user_order_items = OrderItem.objects.filter(order__user_id=self.user.id)
        self.assertEqual(user_order_items.count(), 3)
        self.assertEqual(len(result), user_order_items.count())
        for item in result:
            self.assertTrue(OrderItem.objects.filter(id=item.id).exists())


