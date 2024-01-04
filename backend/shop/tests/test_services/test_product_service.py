from unittest.mock import patch

from django.test import TestCase
from model_bakery import baker
from shop.models import Product
from shop.services import ProductService


class ProductServiceTest(TestCase):
    def setUp(self) -> None:
        self.product = baker.make(Product, title="title")
        self.service = ProductService()

    @patch(
        "shop.services.product_service.ProductRepository."
        "check_if_product_with_same_slug_exists_by_id_and_slug"
    )
    def test_slugify_product_by_id_and_title(self, check_existence_mock):
        check_existence_mock.return_value = False
        result = self.service.slugify_product_by_id_and_title(title="test")
        self.assertEqual(result, "test")
