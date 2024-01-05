from django.contrib.auth import get_user_model
from django.db import models
from django.test import TestCase
from model_bakery import baker
from shop.models import Order


class OrderModelTest(TestCase):
    def setUp(self) -> None:
        self.order = baker.make(Order)

    def test_model_is_inherited_from_Model(self):
        self.assertTrue(issubclass(Order, models.Model))

    def test_model_has_correct_attributes(self):
        obj = Order()
        self.assertTrue(hasattr(obj, "id"))
        self.assertTrue(hasattr(obj, "user_id"))
        self.assertTrue(hasattr(obj, "status"))
        self.assertTrue(hasattr(obj, "created_at"))

    def test_create_order_successfully(self):
        user = baker.make(get_user_model())
        order = Order.objects.create(user=user)
        self.assertEqual(order.user.id, user.id)
