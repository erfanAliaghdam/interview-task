from django.contrib.auth import get_user_model
from django.test import TestCase
from shop.api.v1.serializers import UserOrderListSerializer
from shop.models import Order, OrderItem
from model_bakery import baker
from shop.repositories import OrderRepository

order_repository = OrderRepository()


class UserOrderListSerializerTest(TestCase):
    def setUp(self):
        self.user = baker.make(get_user_model())
        self.order = baker.make(Order, user=self.user)
        self.order_items = baker.make(OrderItem, order=self.order, _quantity=2)
        self.total_price = sum(
            order_item.price * order_item.quantity for order_item in self.order_items
        )

    def test_contains_expected_fields(self):
        expected_fields = ["user", "total_price", "order_items"]
        self.assertEqual(set(UserOrderListSerializer.Meta.fields), set(expected_fields))

    def test_user_order_serializer(self):
        expected_data = {
            "user": self.order.user.id,
            "total_price": self.total_price,
            "order_items": [
                {
                    "product": {
                        "id": self.order_items[0].product.id,
                        "title": self.order_items[0].product.title,
                        "created_at": self.order_items[0].product.created_at.strftime(
                            "%Y-%m-%dT%H:%M:%S.%fZ"
                        ),
                        "slug": self.order_items[0].product.slug,
                        "price": str(self.order_items[0].product.price),
                        "description": self.order_items[0].product.description,
                    },
                    "quantity": self.order_items[0].quantity,
                },
                {
                    "product": {
                        "id": self.order_items[1].product.id,
                        "title": self.order_items[1].product.title,
                        "created_at": self.order_items[1].product.created_at.strftime(
                            "%Y-%m-%dT%H:%M:%S.%fZ"
                        ),
                        "slug": self.order_items[1].product.slug,
                        "price": str(self.order_items[1].product.price),
                        "description": self.order_items[1].product.description,
                    },
                    "quantity": self.order_items[1].quantity,
                },
            ],
        }
        order = order_repository.get_order_with_all_data_and_total_price_by_user_id(
            user_id=self.user
        )
        serializer = UserOrderListSerializer(order.first())
        self.assertEqual(serializer.data["user"], expected_data["user"])
        self.assertEqual(serializer.data["total_price"], expected_data["total_price"])
        self.assertEqual(
            serializer.data["order_items"][0]["product"]["id"],
            expected_data["order_items"][0]["product"]["id"],
        )
        self.assertEqual(
            serializer.data["order_items"][0]["product"]["title"],
            expected_data["order_items"][0]["product"]["title"],
        )
        self.assertEqual(
            serializer.data["order_items"][0]["product"]["created_at"],
            expected_data["order_items"][0]["product"]["created_at"],
        )
        self.assertEqual(
            serializer.data["order_items"][0]["product"]["slug"],
            expected_data["order_items"][0]["product"]["slug"],
        )
        self.assertEqual(
            serializer.data["order_items"][0]["product"]["price"],
            expected_data["order_items"][0]["product"]["price"],
        )
        self.assertEqual(
            serializer.data["order_items"][0]["product"]["description"],
            expected_data["order_items"][0]["product"]["description"],
        )
        self.assertEqual(
            serializer.data["order_items"][0]["quantity"],
            expected_data["order_items"][0]["quantity"],
        )
        self.assertEqual(
            serializer.data["order_items"][0]["product"]["id"],
            expected_data["order_items"][0]["product"]["id"],
        )
