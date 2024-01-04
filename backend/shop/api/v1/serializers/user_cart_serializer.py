from rest_framework import serializers
from shop.api.v1.serializers import ProductDetailSerializer
from shop.models import CartItem, Cart


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductDetailSerializer()

    class Meta:
        model = CartItem
        fields = ["product", "quantity"]


class UserCartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(source="items", many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    items_count = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["user", "cart_items", "total_price", "items_count"]

    def get_total_price(self, obj):
        return obj.total_price

    def get_items_count(self, obj):
        return obj.items_count
