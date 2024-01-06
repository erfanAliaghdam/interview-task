from django.contrib.auth import get_user_model
from django.test import TestCase
from shop.api.v1.serializers import UserCartSerializer
from shop.models import CartItem, Cart
from model_bakery import baker
from shop.repositories import CartRepository

cart_repository = CartRepository()


class UserCartSerializerTest(TestCase):
    def setUp(self):
        self.user = baker.make(get_user_model())
        self.cart = Cart.objects.filter(user_id=self.user.id).first()
        self.cart_items = baker.make(CartItem, cart=self.cart, _quantity=2)
        self.cart_items[0].product.stock = 0
        self.cart_items[1].product.stock = 1
        self.cart_items[1].product.save()
        self.cart_items[0].product.save()

        self.total_price = (
            self.cart_items[1].product.price * self.cart_items[1].quantity
        )

    def test_contains_expected_fields(self):
        expected_fields = [
            "user",
            "total_price",
            "items_count",
            "in_stock_items_count",
            "out_of_stock_products",
            "in_stock_products",
        ]
        self.assertEqual(set(UserCartSerializer.Meta.fields), set(expected_fields))

    def test_user_cart_serializer(self):
        expected_data = {
            "user": self.cart.user.id,
            "total_price": self.total_price,
            "items_count": 2,
            "in_stock_items_count": 1,
            "in_stock_products": [
                {
                    "product": {
                        "id": self.cart_items[1].product.id,
                        "title": self.cart_items[1].product.title,
                        "created_at": self.cart_items[1].product.created_at.strftime(
                            "%Y-%m-%dT%H:%M:%S.%fZ"
                        ),
                        "slug": self.cart_items[1].product.slug,
                        "price": str(self.cart_items[1].product.price),
                        "description": self.cart_items[1].product.description,
                    },
                    "quantity": self.cart_items[1].quantity,
                }
            ],
            "out_of_stock_products": [
                {
                    "product": {
                        "id": self.cart_items[0].product.id,
                        "title": self.cart_items[0].product.title,
                        "created_at": self.cart_items[0].product.created_at.strftime(
                            "%Y-%m-%dT%H:%M:%S.%fZ"
                        ),
                        "slug": self.cart_items[0].product.slug,
                        "price": str(self.cart_items[0].product.price),
                        "description": self.cart_items[0].product.description,
                    },
                    "quantity": self.cart_items[0].quantity,
                }
            ],
        }
        cart = cart_repository.get_cart_with_all_data_and_total_price_by_user_id(
            user_id=self.user
        )
        serializer = UserCartSerializer(cart)
        self.assertEqual(serializer.data["user"], expected_data["user"])
        self.assertEqual(serializer.data["total_price"], expected_data["total_price"])
        self.assertEqual(serializer.data["items_count"], expected_data["items_count"])
        self.assertEqual(
            serializer.data["in_stock_products"][0]["product"]["id"],
            expected_data["in_stock_products"][0]["product"]["id"],
        )
        self.assertEqual(
            serializer.data["in_stock_products"][0]["product"]["title"],
            expected_data["in_stock_products"][0]["product"]["title"],
        )
        self.assertEqual(
            serializer.data["in_stock_products"][0]["product"]["created_at"],
            expected_data["in_stock_products"][0]["product"]["created_at"],
        )
        self.assertEqual(
            serializer.data["in_stock_products"][0]["product"]["slug"],
            expected_data["in_stock_products"][0]["product"]["slug"],
        )
        self.assertEqual(
            serializer.data["in_stock_products"][0]["product"]["price"],
            expected_data["in_stock_products"][0]["product"]["price"],
        )
        self.assertEqual(
            serializer.data["in_stock_products"][0]["product"]["description"],
            expected_data["in_stock_products"][0]["product"]["description"],
        )
        self.assertEqual(
            serializer.data["in_stock_products"][0]["quantity"],
            expected_data["in_stock_products"][0]["quantity"],
        )
        self.assertEqual(
            serializer.data["out_of_stock_products"][0]["product"]["id"],
            expected_data["out_of_stock_products"][0]["product"]["id"],
        )
        self.assertEqual(
            serializer.data["out_of_stock_products"][0]["product"]["title"],
            expected_data["out_of_stock_products"][0]["product"]["title"],
        )
        self.assertEqual(
            serializer.data["in_stock_products"][0]["product"]["created_at"],
            expected_data["in_stock_products"][0]["product"]["created_at"],
        )
        self.assertEqual(
            serializer.data["out_of_stock_products"][0]["product"]["slug"],
            expected_data["out_of_stock_products"][0]["product"]["slug"],
        )
        self.assertEqual(
            serializer.data["out_of_stock_products"][0]["product"]["price"],
            expected_data["out_of_stock_products"][0]["product"]["price"],
        )
        self.assertEqual(
            serializer.data["out_of_stock_products"][0]["product"]["description"],
            expected_data["out_of_stock_products"][0]["product"]["description"],
        )
        self.assertEqual(
            serializer.data["out_of_stock_products"][0]["quantity"],
            expected_data["out_of_stock_products"][0]["quantity"],
        )
