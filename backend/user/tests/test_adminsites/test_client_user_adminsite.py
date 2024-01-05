from django.contrib.admin import AdminSite
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.test import TestCase
from model_bakery import baker
from rest_framework.test import APIClient
from user.adminsites import ClientUserAdmin


class ClientUserAdminTest(TestCase):
    def setUp(self) -> None:
        author_group = baker.make(Group, name="Client")
        self.users = baker.make(get_user_model(), _quantity=5)
        self.users[0].groups.add(author_group)
        self.users[0].save()
        self.client = APIClient()
        self.request = self.client.request()
        self.site = AdminSite()

    def test_class_is_inherited_from_UserAdmin(self):
        self.assertTrue(issubclass(ClientUserAdmin, UserAdmin))

    def test_if_queryset_is_correct(self):
        client = ClientUserAdmin(model=get_user_model(), admin_site=self.site)
        clients = client.get_queryset(self.request)
        self.assertEqual(clients.first().email, self.users[0].email)
