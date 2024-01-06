from django.urls import reverse
from model_bakery import baker
from core.tests.base_test_class import BaseAPITestClass
from shop.models import Order, OrderItem


class UserOrderListViewTest(BaseAPITestClass):
    def setUp(self) -> None:
        super().setUp()
        self.url = reverse("orders-list")
        self.authenticate_user(self.user)
        self.order = baker.make(Order, user_id=self.user.id)
        self.order_items = baker.make(OrderItem, order=self.order, _quantity=4)

    def test_if_unauthorized_user_cannot_access_returns_401(self):
        self.client.logout()
        result = self.client.get(self.url)
        self.assertEqual(result.status_code, 401)
        self.assertEqual(result.data["status"], "failed")
        self.assertEqual(result.data["message"], "Please login.")

    def test_if_user_can_access_cart_list_successfully_returns_200(self):
        result = self.client.get(self.url)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data["status"], "success")
        self.assertEqual(result.data["message"], "user orders retrieved successfully.")
        self.assertEqual(
            result.data["count"], Order.objects.filter(user=self.user).count()
        )
        self.assertIn("data", result.data)
