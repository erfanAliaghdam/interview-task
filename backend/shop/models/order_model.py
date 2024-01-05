from django.contrib.auth import get_user_model
from django.db import models
from shop.models import Product


class Order(models.Model):
    PENDING = 0
    CHECKED = 1
    STATUS_CHOICES = (
        (PENDING, "Pending"),
        (CHECKED, "Checked")
    )

    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="order"
    )
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.order.user.email

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
