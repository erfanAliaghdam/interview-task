from rest_framework import serializers
from shop.models import Product


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "created_at", "slug", "price", "stock"]
