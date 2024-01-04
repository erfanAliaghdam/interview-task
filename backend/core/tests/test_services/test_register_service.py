from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.test import TestCase
from model_bakery import baker

from core.exceptions import Custom500Exception
from core.services import RegisterUserService


class RegisterUserServiceTest(TestCase):
    def setUp(self) -> None:
        self.service = RegisterUserService()
        self.valid_data = {
            "first_name": "test first name",
            "last_name": "test last name",
            "email": "valid-test-user@example.com",
            "password": "Pass123@#$",
        }
        self.user = baker.make(get_user_model())

    @patch("core.services.register_service.UserRepository.register_client_user")
    def test_register_client_user_successfully(self, user_repository_mock):
        user_repository_mock.return_value = self.user
        user = self.service.register_client_user(
            first_name=self.valid_data["first_name"],
            last_name=self.valid_data["last_name"],
            email=self.valid_data["email"],
            password=self.valid_data["password"],
        )
        user_repository_mock.assert_called_once_with(
            first_name=self.valid_data["first_name"],
            last_name=self.valid_data["last_name"],
            email=self.valid_data["email"],
            password=self.valid_data["password"],
        )

    @patch("core.services.register_service.logging")
    @patch("core.services.register_service.UserRepository.register_client_user")
    def test_register_client_user_raise_500_exception(
        self, user_repository_mock, logging_mock
    ):
        user_repository_mock.side_effect = Exception("Simulated exception")

        with self.assertRaises(Custom500Exception):
            self.service.register_client_user(
                first_name=self.valid_data["first_name"],
                last_name=self.valid_data["last_name"],
                email=self.valid_data["email"],
                password=self.valid_data["password"],
            )
            user_repository_mock.assert_called_once_with(
                first_name=self.valid_data["first_name"],
                last_name=self.valid_data["last_name"],
                email=self.valid_data["email"],
                password=self.valid_data["password"],
            )
            logging_mock.assert_called_once()
