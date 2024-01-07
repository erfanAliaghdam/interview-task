from unittest.mock import patch
from django.urls import reverse
from core.tests.base_test_class import BaseSellerUserAPITestClass
import logging

logging.disable(logging.WARNING)


class SaleUserCreateProductTaskViewTest(BaseSellerUserAPITestClass):
    def setUp(self) -> None:
        super().setUp()
        self.authenticate_user(self.user)
        self.url = reverse("sale-products-create")
        self.valid_data = {
            "title": "macbook pro 2023",
            "description": "test description for product",
            "price": 22.5,
            "stock": 25,
        }
        self.invalid_data = {
            "title": "macbook pro 2023",
            "description": "test description for product",
            "stock": 25,
        }

    def test_if_non_seller_user_cannot_access_returns_403(self):
        self.user.groups.clear()
        result = self.client.get(self.url)
        self.assertEqual(result.status_code, 403)
        self.assertEqual(result.data["status"], "failed")
        self.assertEqual(
            result.data["message"], "You are not allowed to do this action."
        )

    def test_if_unauthorized_user_cannot_access_returns_401(self):
        self.client.logout()
        result = self.client.post(self.url)
        self.assertEqual(result.status_code, 401)
        self.assertEqual(result.data["status"], "failed")
        self.assertEqual(result.data["message"], "Please login.")

    def test_if_invalid_data_returns_400(self):
        result = self.client.post(self.url, data=self.invalid_data)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.data["status"], "failed")
        self.assertEqual(result.data["message"], "product creation failed.")

    @patch(
        "shop.api.v1.views.sale.user_create_product_view.ProductRepository."
        "create_product"
    )
    def test_if_user_can_add_to_cart_successfully_returns_200(
        self, create_product_mock
    ):
        create_product_mock.return_value = True
        result = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data["status"], "success")
        self.assertEqual(result.data["message"], "product created successfully.")
