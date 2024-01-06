from django.contrib.auth import get_user_model
from django.test import TestCase
from model_bakery import baker
from shop.models import Product, Cart, CartItem
from shop.repositories import CartRepository


class CartRepositoryTest(TestCase):
    def setUp(self) -> None:
        title = "test"
        self.user = baker.make(get_user_model())
        self.product = baker.make(Product, title=title, price=250, stock=3)
        self.repository = CartRepository()
        self.cart = Cart.objects.filter(user_id=self.user.id).first()
        self.in_stock_cart_item = baker.make(
            CartItem, product=self.product, cart=self.cart, quantity=2
        )
        self.out_of_stock_product = baker.make(Product, stock=0)
        self.out_of_stock_cart_item = baker.make(
            CartItem, product=self.out_of_stock_product, cart=self.cart
        )

    def test_add_product_to_cart_by_user_id_and_product_id(self):
        result = self.repository.add_product_to_cart_by_user_id_and_product_id(
            product_id=self.in_stock_cart_item.product.id, cart_id=self.cart.id
        )
        # check if quantity raises
        self.assertTrue(result)
        self.assertEqual(
            CartItem.objects.filter(
                cart__user=self.user, product_id=self.in_stock_cart_item.product.id
            )
            .first()
            .quantity,
            self.in_stock_cart_item.quantity + 1,
        )

        result = self.repository.add_product_to_cart_by_user_id_and_product_id(
            product_id=self.in_stock_cart_item.product.id, cart_id=self.cart.id
        )
        # check if quantity raises
        self.assertFalse(result)

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
            baker.make(CartItem, cart=self.cart, quantity=1, product=product)

        for product in out_of_stock_products:
            baker.make(CartItem, cart=self.cart, quantity=5, product=product)

        result = self.repository.validate_cart_item_quantity_by_queryset(
            cart_items=CartItem.objects.all()
        )
        self.assertFalse(result)
        CartItem.objects.filter(product__stock=0).delete()
        result = self.repository.validate_cart_item_quantity_by_queryset(
            cart_items=CartItem.objects.all()
        )
        self.assertTrue(result)

    def test_decrease_product_quantity_from_cart_by_user_id_and_product_id(self):
        # successfully decrease
        quantity = self.in_stock_cart_item.quantity
        result = self.repository.decrease_product_quantity_from_cart_by_user_id_and_product_id(
            user_id=self.user, product_id=self.in_stock_cart_item.product.id
        )
        self.assertTrue(result)
        self.in_stock_cart_item.refresh_from_db()
        self.assertEqual(self.in_stock_cart_item.quantity, quantity - 1)
        # cart item quantity = 0
        self.in_stock_cart_item.quantity = 0
        self.in_stock_cart_item.save()
        result = self.repository.decrease_product_quantity_from_cart_by_user_id_and_product_id(
            user_id=self.user, product_id=self.in_stock_cart_item.product.id
        )
        self.assertTrue(result)
        # cart item quantity = 1
        self.in_stock_cart_item.quantity = 1
        self.in_stock_cart_item.save()
        result = self.repository.decrease_product_quantity_from_cart_by_user_id_and_product_id(
            user_id=self.user, product_id=self.in_stock_cart_item.product.id
        )
        self.assertTrue(result)
        self.assertFalse(
            CartItem.objects.filter(id=self.in_stock_cart_item.id).exists()
        )
        result = self.repository.decrease_product_quantity_from_cart_by_user_id_and_product_id(
            user_id=self.user, product_id=self.in_stock_cart_item.product.id
        )
        self.assertFalse(result)
