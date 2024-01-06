from unittest.mock import patch
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

    def test__filter_by_search_term(self):
        search_key = "big blue ball"
        baker.make(Product, title=search_key)
        products = Product.objects.filter(title=search_key)
        result = self.repository._filter_by_search_term(
            queryset=products, search_term=search_key
        )
        self.assertEqual(result.count(), 1)
        self.assertEqual(result.first().id, products.first().id)

    def test__filter_by_in_stock(self):
        product = baker.make(Product, stock=5)
        products = Product.objects.filter(id=product.id)
        result = self.repository._filter_by_in_stock(queryset=products, in_stock=True)
        self.assertEqual(result.count(), 1)
        self.assertEqual(result.first().id, products.first().id)
        product = baker.make(Product, stock=0)
        products = Product.objects.filter(id=product.id)
        result = self.repository._filter_by_in_stock(queryset=products, in_stock=False)
        self.assertEqual(result.count(), 1)
        self.assertEqual(result.first().id, products.first().id)

    @patch(
        "shop.repositories.product_repository.ProductRepository._filter_by_search_term"
    )
    @patch("shop.repositories.product_repository.ProductRepository._filter_by_in_stock")
    @patch("shop.repositories.product_repository.ProductRepository.get_all_products")
    def test_get_all_products_by_filters(
        self, get_all_products_mock, filter_by_in_stock_mock, filter_by_search_term_mock
    ):
        Product.objects.all().delete()
        products = baker.make(Product, stock=3, title="search")
        products = Product.objects.all()
        get_all_products_mock.return_value = products
        filter_by_in_stock_mock.return_value = products
        filter_by_search_term_mock.return_value = products
        self.repository.get_all_products_by_filters()
        self.assertEqual(get_all_products_mock.call_count, 1)
        self.assertEqual(filter_by_in_stock_mock.call_count, 0)
        self.assertEqual(filter_by_search_term_mock.call_count, 0)
        self.repository.get_all_products_by_filters(search_term="xx")
        self.assertEqual(get_all_products_mock.call_count, 2)
        self.assertEqual(filter_by_in_stock_mock.call_count, 0)
        self.assertEqual(filter_by_search_term_mock.call_count, 1)
        self.repository.get_all_products_by_filters(in_stock=True)
        self.assertEqual(get_all_products_mock.call_count, 3)
        self.assertEqual(filter_by_in_stock_mock.call_count, 1)
        self.assertEqual(filter_by_search_term_mock.call_count, 1)
        self.repository.get_all_products_by_filters(in_stock=True, search_term="xx")
        self.assertEqual(get_all_products_mock.call_count, 4)
        self.assertEqual(filter_by_in_stock_mock.call_count, 2)
        self.assertEqual(filter_by_search_term_mock.call_count, 2)
