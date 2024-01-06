from unittest.mock import patch
from django.urls import reverse
from model_bakery import baker
from core.tests.base_test_class import BaseAPITestClass
from shop.models import Cart, CartItem


class UserMakeOrderViewTest(BaseAPITestClass):
    def setUp(self) -> None:
        super().setUp()
        self.url = reverse("cart-order")
        self.authenticate_user(self.user)
        self.cart = Cart.objects.filter(user_id=self.user.id).first()
        self.cart_items = baker.make(CartItem, cart=self.cart, _quantity=4)

    def test_if_unauthorized_user_cannot_access_returns_401(self):
        self.client.logout()
        result = self.client.get(self.url)
        self.assertEqual(result.status_code, 401)
        self.assertEqual(result.data["status"], "failed")
        self.assertEqual(result.data["message"], "Please login.")

    @patch("shop.api.v1.views.user_make_order_view.OrderService" ".place_order")
    def test_if_authorized_user_can_place_order_successfully_returns_200(
        self, place_order_mock
    ):
        place_order_mock.return_value = True
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "success")
        self.assertEqual(response.data["message"], "your order placed successfully.")
