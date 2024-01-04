from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group


class UserRepository:
    def __init__(self):
        self.user_model = get_user_model()

    def filter_user_by_email(self, email: str):
        return self.user_model.objects.filter(email=email)

    def check_if_client_user_exists(self, email: str):
        if self.filter_user_by_email(email).exists():
            return True
        return False

    def register_client_user(
        self, first_name: str, last_name: str, email: str, password: str
    ):
        user = self.user_model.objects.create_user(
            first_name=first_name, last_name=last_name, email=email, password=password
        )
        client_group = Group.objects.filter(name="Client").first()
        user.groups.add(client_group)
        user.refresh_from_db()
        return user
