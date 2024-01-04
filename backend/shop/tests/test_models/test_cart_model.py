from django.contrib.auth import get_user_model
from django.db import models
from django.test import TestCase
from model_bakery import baker
from shop.models import Cart


class CartModelTest(TestCase):
    def setUp(self) -> None:
        self.cart = baker.make(Cart)

    def test_model_is_inherited_from_Model(self):
        self.assertTrue(issubclass(Cart, models.Model))

    def test_model_has_correct_attributes(self):
        obj = Cart()
        self.assertTrue(hasattr(obj, "id"))
        self.assertTrue(hasattr(obj, "user_id"))

    def test_create_cart_successfully(self):
        user = baker.make(get_user_model())
        cart = Cart.objects.create(user=user)
        self.assertEqual(cart.user.id, user.id)
