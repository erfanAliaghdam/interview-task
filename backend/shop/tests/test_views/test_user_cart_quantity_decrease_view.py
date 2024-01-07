from unittest.mock import patch

from django.urls import reverse
from model_bakery import baker
from core.tests.base_test_class import BaseClientUserAPITestClass
from shop.models import Cart, CartItem, Product


class UserDecreaseQuantityCartViewTest(BaseClientUserAPITestClass):
    def setUp(self) -> None:
        super().setUp()
        self.product = baker.make(Product, stock=10)
        self.url = reverse("client-cart-decrease", kwargs={"slug": self.product.slug})
        self.authenticate_user(self.user)
        self.cart = Cart.objects.filter(user_id=self.user.id).first()
        self.cart_items = baker.make(CartItem, cart=self.cart, _quantity=4)

    def test_if_non_client_user_cannot_access_returns_403(self):
        self.user.groups.clear()
        result = self.client.get(self.url)
        self.assertEqual(result.status_code, 403)
        self.assertEqual(result.data["status"], "failed")
        self.assertEqual(
            result.data["message"], "You are not allowed to do this action."
        )

    def test_if_unauthorized_user_cannot_access_returns_401(self):
        self.client.logout()
        result = self.client.post(self.url)
        self.assertEqual(result.status_code, 401)
        self.assertEqual(result.data["status"], "failed")
        self.assertEqual(result.data["message"], "Please login.")

    @patch(
        "shop.api.v1.views.client.user_cart_quantity_decrease_view.ProductRepository."
        "get_product_by_slug"
    )
    @patch(
        "shop.api.v1.views.client.user_cart_quantity_decrease_view.CartService."
        "decrease_product_quantity_on_cart_by_user_id_and_product_id"
    )
    def test_if_user_can_add_to_cart_successfully_returns_200(
        self, decrease_service_mock, product_mock
    ):
        decrease_service_mock.return_value = True
        product_mock.return_value = self.product
        result = self.client.post(self.url)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data["status"], "success")
        self.assertEqual(
            result.data["message"], "product quantity decreased successfully."
        )

    @patch(
        "shop.api.v1.views.client.user_cart_quantity_decrease_view.ProductRepository."
        "get_product_by_slug"
    )
    @patch(
        "shop.api.v1.views.client.user_cart_quantity_decrease_view.CartService."
        "decrease_product_quantity_on_cart_by_user_id_and_product_id"
    )
    def test_if_out_of_stock_product_returns_400(
        self, decrease_service_mock, product_mock
    ):
        decrease_service_mock.return_value = False
        product_mock.return_value = self.product
        self.cart_items[0].product.stock = 0
        self.cart_items[0].product.save()
        result = self.client.post(self.url)
        self.assertEqual(result.status_code, 404)
        self.assertEqual(result.data["status"], "failed")
        self.assertEqual(result.data["message"], "product not found.")

    @patch(
        "shop.api.v1.views.client.user_cart_quantity_decrease_view."
        "ProductRepository.get_product_by_slug"
    )
    def test_if_not_found_product_returns_404(self, product_mock):
        product_mock.return_value = None
        result = self.client.post(self.url)
        self.assertEqual(result.status_code, 404)
        self.assertEqual(result.data["status"], "failed")
        self.assertEqual(result.data["message"], "product not found.")
