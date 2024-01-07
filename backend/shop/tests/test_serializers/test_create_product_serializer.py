from django.test import TestCase

from shop.api.v1.serializers import ProductCreateSerializer


class SaleCreateProductSerializerTest(TestCase):
    def setUp(self) -> None:
        self.valid_data = {
            "title": "macbook pro 2023",
            "description": "test description for product",
            "price": 22.5,
            "stock": 25,
        }

    def test_correct_fields(self):
        expected_fields = ["title", "description", "price", "stock"]
        self.assertEqual(set(ProductCreateSerializer.Meta.fields), set(expected_fields))

    def test_validate_valid_data(self):
        serializer = ProductCreateSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_title(self):
        self.valid_data["title"] = None
        serializer = ProductCreateSerializer(data=self.valid_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors["title"][0], "title is invalid.")

    def test_title_is_required(self):
        del self.valid_data["title"]
        serializer = ProductCreateSerializer(data=self.valid_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors["title"][0], "title is required.")

    def test_invalid_description(self):
        self.valid_data["description"] = None
        serializer = ProductCreateSerializer(data=self.valid_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors["description"][0], "description is invalid.")

    def test_description_is_required(self):
        del self.valid_data["description"]
        serializer = ProductCreateSerializer(data=self.valid_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors["description"][0], "description is required."
        )

    def test_invalid_price(self):
        self.valid_data["price"] = "invalid"
        serializer = ProductCreateSerializer(data=self.valid_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors["price"][0], "price is invalid.")

    def test_invalid_null_price(self):
        self.valid_data["price"] = None
        serializer = ProductCreateSerializer(data=self.valid_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors["price"][0], "price is invalid.")

    def test_price_is_required(self):
        del self.valid_data["price"]
        serializer = ProductCreateSerializer(data=self.valid_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors["price"][0], "price is required.")

    def test_stock_is_invalid(self):
        self.valid_data["stock"] = "invalid"
        serializer = ProductCreateSerializer(data=self.valid_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors["stock"][0], "stock is invalid.")

    def test_validate_stock_cannot_be_less_than_1(self):
        self.valid_data["stock"] = 0
        serializer = ProductCreateSerializer(data=self.valid_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors["stock"][0], "minimum accepted stock value is 1."
        )
