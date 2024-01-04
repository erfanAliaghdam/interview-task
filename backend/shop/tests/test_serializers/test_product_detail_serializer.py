from django.test import TestCase
from shop.api.v1.serializers import ProductDetailSerializer
from shop.models import Product
from model_bakery import baker


class ProductDetailSerializerTest(TestCase):
    def setUp(self):
        self.product = baker.make(Product)

    def test_contains_expected_fields(self):
        serializer = ProductDetailSerializer(instance=self.product)
        data = serializer.data
        self.assertEqual(
            set(data.keys()),
            {"id", "title", "description", "slug", "created_at", "price"},
        )

    def test_product_list_serializer(self):
        expected_data = [
            {
                "id": self.product.id,
                "title": self.product.title,
                "description": self.product.description,
                "created_at": self.product.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "slug": self.product.slug,
                "price": self.product.price,
            }
        ]

        serializer = ProductDetailSerializer(instance=self.product)

        self.assertEqual(serializer.data.get("id"), expected_data[0].get("id"))
        self.assertEqual(serializer.data.get("title"), expected_data[0].get("title"))
        self.assertEqual(serializer.data.get("slug"), expected_data[0].get("slug"))
        self.assertEquals(
            serializer.data.get("price"), str(expected_data[0].get("price"))
        )
        self.assertEqual(
            serializer.data.get("description"), expected_data[0].get("description")
        )
        self.assertEqual(
            serializer.data.get("created_at"), expected_data[0].get("created_at")
        )
