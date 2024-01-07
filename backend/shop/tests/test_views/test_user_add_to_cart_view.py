from django.urls import reverse
from model_bakery import baker
from core.tests.base_test_class import BaseClientUserAPITestClass
from shop.models import Cart, CartItem, Product


class ProductAddToCartViewTest(BaseClientUserAPITestClass):
    def setUp(self) -> None:
        super().setUp()
        self.product = baker.make(Product, stock=10)
        self.url = reverse("cart-add", kwargs={"slug": self.product.slug})
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

    def test_if_user_can_add_to_cart_successfully_returns_200(self):
        result = self.client.post(self.url)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data["status"], "success")
        self.assertEqual(
            result.data["message"], "product added to user cart successfully."
        )

    def test_if_out_of_stock_product_returns_412(self):
        self.product.stock = 0
        self.product.save()
        result = self.client.post(self.url)
        self.assertEqual(result.status_code, 412)
        self.assertEqual(result.data["status"], "failed")
        self.assertEqual(result.data["message"], "product is out of stock.")
