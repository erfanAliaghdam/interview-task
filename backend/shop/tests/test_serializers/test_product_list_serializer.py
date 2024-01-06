from django.test import TestCase
from shop.api.v1.serializers import ProductListSerializer
from shop.models import Product
from model_bakery import baker


class ProductListSerializerTest(TestCase):
    def setUp(self):
        self.products = baker.make(Product, _quantity=2)

    def test_contains_expected_fields(self):
        serializer = ProductListSerializer(instance=self.products[0])
        data = serializer.data
        self.assertEqual(
            set(data.keys()), {"id", "title", "created_at", "slug", "price", "stock"}
        )

    def test_product_list_serializer(self):
        expected_data = [
            {
                "id": self.products[0].id,
                "title": self.products[0].title,
                "created_at": self.products[0].created_at.strftime(
                    "%Y-%m-%dT%H:%M:%S.%fZ"
                ),
                "slug": self.products[0].slug,
                "price": self.products[0].price,
                "stock": self.products[0].stock,
            },
            {
                "id": self.products[1].id,
                "title": self.products[1].title,
                "created_at": self.products[1].created_at.strftime(
                    "%Y-%m-%dT%H:%M:%S.%fZ"
                ),
                "slug": self.products[1].slug,
                "price": self.products[1].price,
                "stock": self.products[1].stock,
            },
        ]

        serializer = ProductListSerializer(self.products, many=True)
        for idx, item in enumerate(serializer.data):
            self.assertEqual(item.get("id"), expected_data[idx].get("id"))
            self.assertEqual(item.get("title"), expected_data[idx].get("title"))
            self.assertEqual(
                item.get("created_at"), expected_data[idx].get("created_at")
            )
            self.assertEqual(item.get("slug"), expected_data[idx].get("slug"))
            self.assertEqual(item.get("price"), str(expected_data[idx].get("price")))
            self.assertEqual(item.get("stock"), expected_data[idx].get("stock"))
