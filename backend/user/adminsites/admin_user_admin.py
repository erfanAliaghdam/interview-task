from django.contrib.auth.admin import UserAdmin


class AdminUserAdmin(UserAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "user_identifier",
        "is_active",
        "is_staff",
    )
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
        return queryset.filter(is_staff=True)
