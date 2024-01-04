from django.test import TestCase
from model_bakery import baker

from shop.models import Product
from shop.repositories import ProductRepository


class ProductRepositoryTest(TestCase):
    def setUp(self) -> None:
        title = "test"
        self.product = baker.make(Product, title=title)
        self.repository = ProductRepository()

    def test_check_if_product_with_same_slug_exists_by_id_and_slug_with_existing_product_id(
        self,
    ):
        self.assertTrue(
            self.repository.check_if_product_with_same_slug_exists_by_id_and_slug(
                product_id=self.product.id, slug=self.product.slug
            )
        )
        self.assertTrue(
            self.repository.check_if_product_with_same_slug_exists_by_id_and_slug(
                slug=self.product.title
            )
        )
        self.assertFalse(
            self.repository.check_if_product_with_same_slug_exists_by_id_and_slug(
                product_id=self.product.id, slug="xx"
            )
        )
