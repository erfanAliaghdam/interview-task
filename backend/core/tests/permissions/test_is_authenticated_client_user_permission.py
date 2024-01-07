from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.http import HttpRequest
from django.test import TestCase
from model_bakery import baker
from rest_framework.views import APIView
from core.exceptions import Custom403Exception
from core.permissions import IsAuthenticatedPermission
from core.permissions.client import IsAuthenticatedActiveClientUserPermission
from unittest.mock import MagicMock


class IsAuthenticatedActiveClientUserPermissionTest(TestCase):
    def setUp(self) -> None:
        self.user = baker.make(get_user_model(), is_active=True)
        self.request = HttpRequest()
        self.request.user = self.user
        self.client_group = baker.make(Group, name="Client")
        self.user.groups.add(self.client_group)

    def test_permission_is_inherited_from_correct_class(self):
        self.assertTrue(
            issubclass(
                IsAuthenticatedActiveClientUserPermission, IsAuthenticatedPermission
            )
        )

    def test_has_permission_client_user(self):
        permission = IsAuthenticatedActiveClientUserPermission()

        result = permission.has_permission(self.request, APIView())

        self.assertTrue(result)

    def test_has_no_permission_non_publisher_user(self):
        permission = IsAuthenticatedActiveClientUserPermission()
        self.user.groups.clear()
        self.request = MagicMock()
        self.request.user = self.user
        self.request.is_authenticated = True
        with self.assertRaises(Custom403Exception):
            permission.has_permission(self.request, APIView())
