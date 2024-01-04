from django.contrib import admin
from django.contrib.auth import get_user_model
from user.adminsites import (
    ClientUserAdmin,
    AdminUserAdmin,
)
from user.models.proxy import ClientProxyModel, AdminProxyModel

admin.site.register(ClientProxyModel, ClientUserAdmin)
admin.site.register(AdminProxyModel, AdminUserAdmin)


@admin.register(get_user_model())
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "user_identifier", "is_active")
    ordering = ["date_joined"]
    list_filter = ["is_active", "date_joined"]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "user_identifier",
                    "first_name",
                    "last_name",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ["email", "first_name", "last_name", "user_identifier"]
    search_help_text = "search by : email, first name, last name, user identifier"