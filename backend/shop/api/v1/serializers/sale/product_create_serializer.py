from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from shop.models import Product


class ProductCreateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        required=True,
        error_messages={
            "required": "title is required.",
            "invalid": "title is invalid.",
            "null": "title is invalid.",
        },
    )

    description = serializers.CharField(
        required=True,
        error_messages={
            "required": "description is required.",
            "invalid": "description is invalid.",
            "null": "description is invalid.",
        },
    )

    price = serializers.DecimalField(
        required=True,
        decimal_places=2,
        max_digits=12,
        error_messages={
            "required": "price is required.",
            "invalid": "price is invalid.",
            "null": "price is invalid.",
        },
    )

    stock = serializers.IntegerField(
        required=False,
        error_messages={
            "required": "stock is required.",
            "invalid": "stock is invalid.",
        },
    )

    class Meta:
        model = Product
        fields = ["title", "description", "price", "stock"]

    def validate_stock(self, stock):
        if stock < 1:
            raise ValidationError("minimum accepted stock value is 1.")
        return stock
