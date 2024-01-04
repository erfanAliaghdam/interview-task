from django.contrib.auth import get_user_model


class AdminProxyModel(get_user_model()):
    class Meta:
        proxy = True
        verbose_name = "Admin user"
        verbose_name_plural = "Admin users"
