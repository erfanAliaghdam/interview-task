from rest_framework import serializers
from shop.api.v1.serializers import ProductDetailSerializer
from shop.models import CartItem, Cart
from shop.repositories import CartRepository


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductDetailSerializer()

    class Meta:
        model = CartItem
        fields = ["product", "quantity"]


class UserCartSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cart_repository = CartRepository()

    total_price = serializers.SerializerMethodField()
    items_count = serializers.SerializerMethodField()
    in_stock_items_count = serializers.SerializerMethodField()
    out_of_stock_products = serializers.SerializerMethodField()
    in_stock_products = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            "user",
            "total_price",
            "items_count",
            "in_stock_items_count",
            "out_of_stock_products",
            "in_stock_products",
        ]

    def get_total_price(self, obj):
        return obj.total_price

    def get_in_stock_items_count(self, obj):
        return obj.in_stock_items_count

    def get_items_count(self, obj):
        return obj.items_count

    def get_in_stock_products(self, obj):
        cart_items = self.cart_repository.get_in_stock_cart_items_by_cart_id(
            cart_id=obj.id
        )
        cart_items = CartItemSerializer(cart_items, many=True)
        return cart_items.data

    def get_out_of_stock_products(self, obj):
        cart_items = self.cart_repository.get_out_of_stock_cart_items_by_cart_id(
            cart_id=obj.id
        )
        cart_items = CartItemSerializer(cart_items, many=True)
        return cart_items.data
