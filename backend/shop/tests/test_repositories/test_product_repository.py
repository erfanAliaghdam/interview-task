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
        self.assertFalse(
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

    def test_get_all_products(self):
        result = self.repository.get_all_products()
        all_products = Product.objects.all()
        self.assertEqual(result.first().id, all_products.first().id)
        self.assertEqual(result.count(), all_products.count())

    def test_get_product_by_slug(self):
        product = self.repository.get_product_by_slug(slug=self.product.slug)
        self.assertEqual(product.id, self.product.id)

    def test_get_products_by_id_list(self):
        products = baker.make(Product, _quantity=3)
        product_ids_list = [product.id for product in products]
        result = self.repository.get_products_by_id_list(product_ids=product_ids_list)
        self.assertEqual(result.count(), len(products))
        for item in result:
            self.assertIn(item.id, product_ids_list)
