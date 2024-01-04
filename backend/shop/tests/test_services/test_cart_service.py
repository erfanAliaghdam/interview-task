from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from model_bakery import baker
from shop.models import Cart, Product
from shop.services import CartService


class CartServiceTest(TestCase):
    def setUp(self) -> None:
        self.user = baker.make(get_user_model())
        self.cart = baker.make(Cart, user=self.user)
        self.product = baker.make(Product)
        self.service = CartService()

    @patch(
        "shop.services.cart_service.CartRepository."
        "add_product_to_cart_by_user_id_and_product_id"
    )
    def test_add_product_to_cart_by_product_id_and_user_id(self, cart_mock):
        cart_mock.return_value = self.cart
        result = self.service.add_product_to_cart_by_product_id_and_user_id(
            product_id=self.product.id, user_id=self.user.id
        )
        self.assertEqual(result, self.cart)
