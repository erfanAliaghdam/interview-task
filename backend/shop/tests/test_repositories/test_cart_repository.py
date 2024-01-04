from django.contrib.auth import get_user_model
from django.test import TestCase
from model_bakery import baker
from shop.models import Product, Cart, CartItem
from shop.repositories import CartRepository


class CartRepositoryTest(TestCase):
    def setUp(self) -> None:
        title = "test"
        self.user = baker.make(get_user_model())
        self.product = baker.make(Product, title=title, price=250)
        self.repository = CartRepository()

    def test_add_product_to_cart_by_user_id_and_product_id(self):
        self.assertFalse(Cart.objects.filter(user=self.user).exists())
        result = self.repository.add_product_to_cart_by_user_id_and_product_id(
            product_id=self.product.id, user_id=self.user.id
        )
        self.assertTrue(Cart.objects.filter(user=self.user).exists())
        self.assertEqual(
            Cart.objects.filter(user=self.user).first().items.all().count(), 1
        )
        self.assertEqual(result.user.id, self.user.id)
        self.repository.add_product_to_cart_by_user_id_and_product_id(
            product_id=self.product.id, user_id=self.user.id
        )
        # check if new cart item not created
        self.assertEqual(
            Cart.objects.filter(user=self.user).first().items.all().count(), 1
        )
        # check if quantity raises
        self.assertEqual(
            Cart.objects.filter(user=self.user).first().items.all().first().quantity, 2
        )

    def test_get_cart_with_all_data_and_total_price_by_user_id(self):
        cart = baker.make(Cart, user=self.user)
        baker.make(CartItem, product=self.product, cart=cart)
        result = self.repository.get_cart_with_all_data_and_total_price_by_user_id(
            user_id=self.user.id
        )
        self.assertEqual(
            result.total_price,
            sum([item.product.price for item in CartItem.objects.filter(cart=cart)]),
        )
        self.assertEqual(result.items_count, CartItem.objects.filter(cart=cart).count())
        self.assertEqual(result.id, cart.id)
