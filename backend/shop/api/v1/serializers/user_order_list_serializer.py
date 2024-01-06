from rest_framework import serializers
from shop.api.v1.serializers import ProductDetailSerializer
from shop.models import Order, OrderItem


class UserOrderItemSerializer(serializers.ModelSerializer):
    product = ProductDetailSerializer()

    class Meta:
        model = OrderItem
        fields = ["quantity", "price", "product"]


class UserOrderListSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    order_items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ["user", "total_price", "order_items"]

    def get_total_price(self, obj):
        return obj.total_price

    def get_order_items(self, obj):
        order_items = UserOrderItemSerializer(obj.items, many=True)
        return order_items.data
