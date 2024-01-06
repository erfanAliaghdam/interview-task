from rest_framework import serializers

from shop.models import Product


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "description", "slug", "created_at", "price", "stock"]
