from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.db import models
from django.test import TestCase
from model_bakery import baker
from shop.models import Order, OrderItem, Product


class OrderItemModelTest(TestCase):
    def setUp(self) -> None:
        self.user = baker.make(get_user_model())
        self.product = baker.make(Product)
        self.order = baker.make(Order)
        self.order_item = baker.make(OrderItem, order=self.order)

    def test_model_is_inherited_from_Model(self):
        self.assertTrue(issubclass(OrderItem, models.Model))

    def test_model_has_correct_attributes(self):
        obj = OrderItem()
        self.assertTrue(hasattr(obj, "id"))
        self.assertTrue(hasattr(obj, "order_id"))
        self.assertTrue(hasattr(obj, "product_id"))
        self.assertTrue(hasattr(obj, "quantity"))
        self.assertTrue(hasattr(obj, "price"))

    def test_create_order_item_successfully(self):
        new_product = baker.make(Product)
        order_item = OrderItem.objects.create(
            order=self.order, product=new_product, quantity=2, price=new_product.price
        )
        self.assertEqual(order_item.order.id, self.order.id)
        self.assertEqual(order_item.product.id, new_product.id)
        self.assertEqual(order_item.quantity, 2)
        self.assertAlmostEqual(order_item.price, new_product.price)

    @patch("shop.models.order_model.user_order_checked_email.delay")
    def test_send_email_on_order_status_change_to_checked(self, email_mock):
        order = baker.make(Order)
        self.assertEqual(email_mock.call_count, 0)
        order.status = Order.PENDING
        order.save()
        self.assertEqual(email_mock.call_count, 0)
        order.status = Order.CHECKED
        order.save()
        self.assertEqual(email_mock.call_count, 1)
        order.status = Order.CHECKED
        order.save()
        self.assertEqual(email_mock.call_count, 1)
