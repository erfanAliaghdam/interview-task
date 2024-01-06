from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.test import TestCase
from model_bakery import baker
from core.exceptions import Custom412Exception
from shop.models import Order, OrderItem, Cart, CartItem, Product
from shop.services import OrderService


class CartServiceTest(TestCase):
    def setUp(self) -> None:
        self.user = baker.make(get_user_model())
        self.order = baker.make(Order, user=self.user)
        self.order_items = baker.make(OrderItem, order=self.order)
        self.cart = Cart.objects.filter(user_id=self.user.id).first()
        self.cart_items = baker.make(CartItem, cart=self.cart, _quantity=2)
        self.out_of_stock_product = baker.make(Product, stock=0)
        self.in_stock_product = baker.make(Product, stock=1)
        self.cart_items[0].product = self.out_of_stock_product
        self.cart_items[1].product = self.in_stock_product
        self.cart_items[0].save()
        self.cart_items[1].save()
        self.service = OrderService()

    @patch("shop.services.order_service.CartRepository.get_cart_items_by_user_id")
    def test_place_order_handles_empty_cart(self, get_cart_items_by_user_id_mock):
        get_cart_items_by_user_id_mock.return_value = None
        with self.assertRaises(Custom412Exception):
            self.service.place_order(user_id=self.user.id)

    @patch("shop.services.order_service.CartRepository.get_cart_items_by_user_id")
    @patch(
        "shop.services.order_service."
        "CartRepository.validate_cart_item_quantity_by_queryset"
    )
    @patch("shop.services.order_service.ProductRepository.get_products_by_id_list")
    def test_place_order_handles_empty_cart(
        self,
        get_products_by_id_list_mock,
        validate_cart_item_quantity_by_queryset_mock,
        get_cart_items_by_user_id_mock,
    ):
        get_products_by_id_list_mock.return_value = Product.objects.all()
        validate_cart_item_quantity_by_queryset_mock.return_value = False
        get_cart_items_by_user_id_mock.return_value = CartItem.objects.all()
        with self.assertRaises(Custom412Exception):
            self.service.place_order(user_id=self.user.id)

    @patch(
        "shop.services.order_service.CartRepository."
        "update_cart_items_products_stock_by_queryset"
    )
    @patch("shop.services.order_service.CartRepository.get_cart_items_by_user_id")
    @patch(
        "shop.services.order_service.CartRepository."
        "validate_cart_item_quantity_by_queryset"
    )
    @patch("shop.services.order_service.ProductRepository.get_products_by_id_list")
    @patch("shop.services.order_service.OrderRepository.create_order")
    @patch(
        "shop.services.order_service.OrderRepository."
        "create_order_items_based_on_cart_items_query"
    )
    def test_all_cart_items_will_be_deleted_at_last(
        self,
        create_order_items_based_on_cart_items_query_mock,
        create_order_mock,
        get_products_by_id_list_mock,
        validate_cart_item_quantity_by_queryset_mock,
        get_cart_items_by_user_id_mock,
        update_cart_items_products_stock_by_queryset_mock,
    ):
        # remove out of stock from cart items
        self.cart_items[0].delete()
        self.cart.refresh_from_db()

        self.assertNotEqual(CartItem.objects.filter(cart__user_id=self.user).count(), 0)
        create_order_items_based_on_cart_items_query_mock.return_value = (
            self.order_items
        )
        create_order_mock.return_value = self.order
        get_products_by_id_list_mock.return_value = Product.objects.all()
        validate_cart_item_quantity_by_queryset_mock.return_value = True
        get_cart_items_by_user_id_mock.return_value = CartItem.objects.filter(
            cart__user_id=self.user
        )
        update_cart_items_products_stock_by_queryset_mock.return_value = True
        self.service.place_order(user_id=self.user.id)
        self.assertEqual(CartItem.objects.filter(cart__user_id=self.user).count(), 0)
