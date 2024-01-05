from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.test import TestCase
from model_bakery import baker
from shop.models import Order, Product, OrderItem
from shop.services import OrderService


class CartServiceTest(TestCase):
    def setUp(self) -> None:
        self.user = baker.make(get_user_model())
        self.order = baker.make(Order, user=self.user)
        self.order_items = baker.make(OrderItem, order=self.order)
        self.service = OrderService()

    @patch("shop.services.order_service.OrderRepository.create_order")
    @patch("shop.services.order_service.OrderRepository"
           ".create_order_items_based_on_cart_items")
    def test_place_order(
        self,
        create_order_by_cart_item_mock,
        create_order_mock
    ):
        create_order_mock.return_value = self.order
        create_order_by_cart_item_mock.return_value = OrderItem.objects.all()
        result = self.service.place_order(user_id=self.user.id)
        self.assertEqual(result, create_order_by_cart_item_mock.return_value)

