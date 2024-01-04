from django.urls import reverse
from model_bakery import baker
from core.tests.base_test_class import BaseAPITestClass
from shop.models import Product
from shop.api.v1.serializers import ProductDetailSerializer


class ProductDetailViewTest(BaseAPITestClass):
    def setUp(self) -> None:
        super().setUp()
        self.product = baker.make(Product)
        self.url = reverse("products-detail", kwargs={"slug": self.product.slug})
        self.authenticate_user(self.user)

    def test_if_unauthorized_user_cannot_access_returns_401(self):
        self.client.logout()
        result = self.client.get(self.url)
        self.assertEqual(result.status_code, 401)
        self.assertEqual(result.data["status"], "failed")
        self.assertEqual(result.data["message"], "Please login.")

    def test_if_authorized_user_can_access_returns_200(self):
        result = self.client.get(self.url)
        serializer = ProductDetailSerializer(instance=self.product)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data["status"], "success")
        self.assertEqual(result.data["message"], "product retrieved successfully.")
        self.assertDictEqual(result.data["data"], serializer.data)

    def test_if_authorized_user_cannot_access_non_existing_returns_404(self):
        url = reverse("products-detail", kwargs={"slug": "invalid"})
        result = self.client.get(url)
        self.assertEqual(result.status_code, 404)
        self.assertEqual(result.data["status"], "failed")
        self.assertEqual(result.data["message"], "product not found.")
