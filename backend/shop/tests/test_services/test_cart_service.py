from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from model_bakery import baker
from shop.models import Cart, Product
from shop.services import CartService


class CartServiceTest(TestCase):
    def setUp(self) -> None:
        self.user = baker.make(get_user_model())
        self.cart = Cart.objects.filter(user_id=self.user.id).first()
        self.product = baker.make(Product)
        self.service = CartService()

    @patch(
        "shop.services.cart_service.CartRepository."
        "add_product_to_cart_by_user_id_and_product_id"
    )
    def test_add_product_to_cart_by_product_id_and_user_id(self, cart_mock):
        cart_mock.return_value = True
        result = self.service.add_product_to_cart_by_product_id_and_user_id(
            product_id=self.product.id, user_id=self.user.id
        )
        self.assertEqual(result, cart_mock.return_value)

    @patch(
        "shop.services.cart_service.CartRepository."
        "decrease_product_quantity_from_cart_by_user_id_and_product_id"
    )
    def test_decrease_product_quantity_on_cart_by_user_id_and_product_id(
        self, decrease_quantity_mock
    ):
        decrease_quantity_mock.return_value = None
        result = (
            self.service.decrease_product_quantity_on_cart_by_user_id_and_product_id(
                user_id=self.user.id, product_id=self.product.id
            )
        )
        self.assertFalse(result)
        decrease_quantity_mock.return_value = True
        result = (
            self.service.decrease_product_quantity_on_cart_by_user_id_and_product_id(
                user_id=self.user.id, product_id=self.product.id
            )
        )
        self.assertTrue(result)
