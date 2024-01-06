from django.urls import path
from core.api.v1.views import (
    register_client_user_view,
    login_client_user_view,
)

urlpatterns = [
    path("auth/register/", register_client_user_view, name="register-client"),
    path("auth/login/", login_client_user_view, name="login-client"),
]
