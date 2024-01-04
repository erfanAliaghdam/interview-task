from _decimal import Decimal

from django.db import models
from django.test import TestCase
from model_bakery import baker

from shop.models import Product


class BookModelTest(TestCase):
    def setUp(self) -> None:
        self.product = baker.make(Product)

    def test_model_is_inherited_from_Model(self):
        self.assertTrue(issubclass(Product, models.Model))

    def test_model_has_correct_attributes(self):
        obj = Product()
        self.assertTrue(hasattr(obj, "id"))
        self.assertTrue(hasattr(obj, "title"))
        self.assertTrue(hasattr(obj, "description"))
        self.assertTrue(hasattr(obj, "price"))
        self.assertTrue(hasattr(obj, "slug"))
        self.assertTrue(hasattr(obj, "created_at"))

    def test_create_book_successfully(self):
        title = "test-xx"
        description = "test"
        price = Decimal(2500.245)
        book = Product.objects.create(title=title, description=description, price=price)
        self.assertEqual(book.title, title)
        self.assertEqual(book.description, description)
        self.assertAlmostEquals(book.price, price)
        self.assertEqual(book.slug, title)

    def test_if_slug_generates_automatically(self):
        title = "test-xx"
        self.assertFalse(Product.objects.filter(slug=title + "-1").exists())
        baker.make(Product, title=title, _quantity=2)
        self.assertTrue(Product.objects.filter(slug=title + "-1").exists())
