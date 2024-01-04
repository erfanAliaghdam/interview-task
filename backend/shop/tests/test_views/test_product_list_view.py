from django.urls import reverse
from model_bakery import baker

from core.tests.base_test_class import BaseAPITestClass
from shop.models import Product


class ProductListViewTest(BaseAPITestClass):
    def setUp(self) -> None:
        super().setUp()
        self.url = reverse("products-list")
        self.authenticate_user(self.user)
        self.products = baker.make(Product, _quantity=4)

    def test_if_unauthorized_user_cannot_access_returns_401(self):
        self.client.logout()
        result = self.client.get(self.url)
        self.assertEqual(result.status_code, 401)
        self.assertEqual(result.data["status"], "failed")
        self.assertEqual(result.data["message"], "Please login.")

    def test_if_authorized_user_can_access_returns_200(self):
        result = self.client.get(self.url)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data["status"], "success")
        self.assertEqual(result.data["message"], "product list retrieved successfully.")
        self.assertEqual(len(result.data["data"]), len(self.products))
        self.assertEqual(result.data["count"], len(self.products))
