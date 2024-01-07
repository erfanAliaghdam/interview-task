from django.contrib.auth import get_user_model


class SellerProxyModel(get_user_model()):
    class Meta:
        proxy = True
        verbose_name = "Seller user"
        verbose_name_plural = "Seller users"
