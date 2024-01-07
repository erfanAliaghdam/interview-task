from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group


class SellerUserAdmin(UserAdmin):
    list_display = ("email", "first_name", "last_name", "user_identifier", "is_active")
    ordering = ["date_joined"]
    list_filter = ["is_active", "date_joined"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
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

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(groups__name="Sale")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Check if the user is being created (not modified)
        if not change:
            # Get or create the "Sale" group
            seller_group, created = Group.objects.get_or_create(name="Sale")

            # Add the user to the "Sale" group
            obj.groups.add(seller_group)
