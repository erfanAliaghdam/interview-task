from django.contrib.auth import get_user_model
from django.db import models
from shop.models import Product


class Cart(models.Model):
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, related_name="cart"
    )

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.cart.user.email

    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
        unique_together = ("product", "cart")
