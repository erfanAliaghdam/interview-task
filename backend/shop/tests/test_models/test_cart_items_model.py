from django.contrib.auth import get_user_model
from django.db import models
from django.test import TestCase
from model_bakery import baker
from shop.models import Cart, CartItem, Product


class CartItemModelTest(TestCase):
    def setUp(self) -> None:
        self.user = baker.make(get_user_model())
        self.product = baker.make(Product)
        self.cart = Cart.objects.filter(user=self.user).first()
        self.cart_item = baker.make(CartItem, cart=self.cart)

    def test_model_is_inherited_from_Model(self):
        self.assertTrue(issubclass(CartItem, models.Model))

    def test_model_has_correct_attributes(self):
        obj = CartItem()
        self.assertTrue(hasattr(obj, "id"))
        self.assertTrue(hasattr(obj, "cart_id"))
        self.assertTrue(hasattr(obj, "product_id"))
        self.assertTrue(hasattr(obj, "quantity"))

    def test_create_cart_item_successfully(self):
        new_product = baker.make(Product)
        cart_item = CartItem.objects.create(
            cart=self.cart, product=new_product, quantity=2
        )
        self.assertEqual(cart_item.cart.id, self.cart.id)
        self.assertEqual(cart_item.product.id, new_product.id)
        self.assertEqual(cart_item.quantity, 2)
