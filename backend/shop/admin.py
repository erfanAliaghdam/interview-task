from django.contrib import admin
from shop.models import Product, Order, OrderItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "created_at", "stock"]
    list_filter = ["created_at"]
    search_fields = ["title"]


class TabularOrderItem(admin.TabularInline):
    model = OrderItem
    autocomplete_fields = ["product"]
    readonly_fields = ["price"]
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["user_email", "created_at", "status"]
    list_filter = ["status", "created_at"]
    list_editable = ["status"]
    inlines = [TabularOrderItem]
    readonly_fields = ["user"]

    def get_queryset(self, request):
        return Order.objects.select_related("user").all()

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = "User Email"
