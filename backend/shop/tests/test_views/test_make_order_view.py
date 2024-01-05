from unittest.mock import patch
from django.urls import reverse
from model_bakery import baker
from core.tests.base_test_class import BaseAPITestClass
from shop.models import Cart, CartItem


class UserMakeOrderViewTest(BaseAPITestClass):
    def setUp(self) -> None:
        super().setUp()
        self.url = reverse("order-make")
        self.authenticate_user(self.user)
        self.cart = baker.make(Cart, user=self.user)
        self.cart_items = baker.make(CartItem, cart=self.cart, _quantity=4)

    def test_if_unauthorized_user_cannot_access_returns_401(self):
        self.client.logout()
        result = self.client.get(self.url)
        self.assertEqual(result.status_code, 401)
        self.assertEqual(result.data["status"], "failed")
        self.assertEqual(result.data["message"], "Please login.")

    @patch("shop.api.v1.views.user_make_order_view.CartRepository"
           ".get_cart_items_by_user_id")
    def test_if_empty_cart_returns_412(self, cart_items_mock):
        cart_items_mock.return_value = None
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 412)
        self.assertEqual(response.data["status"], "failed")
        self.assertEqual(response.data["message"], "your cart is empty.")

    @patch("shop.api.v1.views.user_make_order_view.CartRepository"
           ".get_cart_items_by_user_id")
    def test_if_authorized_user_can_place_order_successfully_returns_200(
            self,
            cart_items_mock
    ):
        cart_items_mock.return_value = CartItem.objects.filter(cart__user_id=self.user.id)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "success")
        self.assertEqual(
            response.data["message"],
            "your order placed successfully.")

    @patch("shop.api.v1.views.user_make_order_view.CartRepository"
           ".get_cart_items_by_user_id")
    @patch("shop.api.v1.views.user_make_order_view.OrderService"
           ".place_order")
    def test_if_handle_exception_returns_500(
            self,
            place_order_mock,
            cart_items_mock
    ):
        place_order_mock.side_effect = Exception("simulated")
        cart_items_mock.return_value = CartItem.objects.filter(cart__user_id=self.user.id)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.data["status"], "failed")
        self.assertEqual(response.data["message"], "Please try again later.")
