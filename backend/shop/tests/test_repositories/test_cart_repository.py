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
        self.cart = baker.make(Cart, user=self.user)
        self.in_stock_cart_item = baker.make(
            CartItem, product=self.product, cart=self.cart
        )
        self.out_of_stock_product = baker.make(Product, stock=0)
        self.out_of_stock_cart_item = baker.make(
            CartItem, product=self.out_of_stock_product, cart=self.cart
        )

    def test_add_product_to_cart_by_user_id_and_product_id(self):
        Cart.objects.all().delete()
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
        result = self.repository.get_cart_with_all_data_and_total_price_by_user_id(
            user_id=self.user.id
        )
        self.assertEqual(
            result.total_price,
            self.in_stock_cart_item.product.price * self.in_stock_cart_item.quantity,
        )
        self.assertEqual(
            result.items_count, CartItem.objects.filter(cart=self.cart).count()
        )
        self.assertEqual(result.id, self.cart.id)
        self.assertEqual(result.in_stock_items_count, 1)

    def test_get_in_stock_cart_items_by_cart_id(self):
        in_stock_cart_items = self.repository.get_in_stock_cart_items_by_cart_id(
            cart_id=self.cart.id
        )
        self.assertEqual(in_stock_cart_items.count(), 1)
        self.assertEqual(in_stock_cart_items.first().id, self.in_stock_cart_item.id)

    def test_get_out_of_stock_cart_items_by_cart_id(self):
        out_of_stock_cart_items = (
            self.repository.get_out_of_stock_cart_items_by_cart_id(cart_id=self.cart.id)
        )
        self.assertEqual(out_of_stock_cart_items.count(), 1)
        self.assertEqual(
            out_of_stock_cart_items.first().id, self.out_of_stock_cart_item.id
        )

    def test_validate_cart_item_quantity_by_queryset(self):
        CartItem.objects.all().delete()
        in_stock_products = baker.make(Product, stock=2, _quantity=2)
        out_of_stock_products = baker.make(Product, stock=0, _quantity=2)
        for product in in_stock_products:
            baker.make(CartItem, quantity=1, product=product)

        for product in out_of_stock_products:
            baker.make(CartItem, quantity=5, product=product)

        result = self.repository.validate_cart_item_quantity_by_queryset(
            cart_items=CartItem.objects.all()
        )
        self.assertFalse(result)
        CartItem.objects.filter(product__stock=0).delete()
        result = self.repository.validate_cart_item_quantity_by_queryset(
            cart_items=CartItem.objects.all()
        )
        self.assertTrue(result)
