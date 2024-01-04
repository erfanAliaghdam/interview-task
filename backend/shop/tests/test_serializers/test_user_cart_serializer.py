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
        self.cart = baker.make(Cart, user=self.user)
        self.cart_items = baker.make(CartItem, cart=self.cart, _quantity=2)
        self.total_price = sum([item.product.price for item in self.cart_items])

    def test_contains_expected_fields(self):
        expected_fields = ["user", "cart_items", "total_price", "items_count"]
        self.assertEqual(set(UserCartSerializer.Meta.fields), set(expected_fields))

    def test_user_cart_serializer(self):
        expected_data = {
            "user": self.cart.user.id,
            "total_price": self.total_price,
            "items_count": 2,
            "cart_items": [
                {
                    "product": {
                        "id": item.product.id,
                        "title": item.product.title,
                        "created_at": item.product.created_at.strftime(
                            "%Y-%m-%dT%H:%M:%S.%fZ"
                        ),
                        "slug": item.product.slug,
                        "price": str(item.product.price),
                        "description": item.product.description,
                    },
                    "quantity": item.quantity,
                }
                for item in self.cart_items
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
            serializer.data["cart_items"][0]["product"]["id"],
            expected_data["cart_items"][0]["product"]["id"],
        )
        self.assertEqual(
            serializer.data["cart_items"][0]["product"]["title"],
            expected_data["cart_items"][0]["product"]["title"],
        )
        self.assertEqual(
            serializer.data["cart_items"][0]["product"]["created_at"],
            expected_data["cart_items"][0]["product"]["created_at"],
        )
        self.assertEqual(
            serializer.data["cart_items"][0]["product"]["slug"],
            expected_data["cart_items"][0]["product"]["slug"],
        )
        self.assertEqual(
            serializer.data["cart_items"][0]["product"]["price"],
            expected_data["cart_items"][0]["product"]["price"],
        )
        self.assertEqual(
            serializer.data["cart_items"][0]["product"]["description"],
            expected_data["cart_items"][0]["product"]["description"],
        )
        self.assertEqual(
            serializer.data["cart_items"][0]["quantity"],
            expected_data["cart_items"][0]["quantity"],
        )
