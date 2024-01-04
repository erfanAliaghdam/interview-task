from django.contrib.auth import get_user_model


class ClientProxyModel(get_user_model()):
    class Meta:
        proxy = True
        verbose_name = "Client user"
        verbose_name_plural = "Client users"
