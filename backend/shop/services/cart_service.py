from shop.models import Cart, CartItem
from shop.repositories import ProductRepository, CartRepository


class CartService:
    def __init__(self, *args, **kwargs):
        self.product_repository = ProductRepository()
        self.cart_repository = CartRepository()

    def add_product_to_cart_by_product_id_and_user_id(
        self, user_id: int, product_id: int
    ):
        cart = self.cart_repository.add_product_to_cart_by_user_id_and_product_id(
            product_id=product_id, user_id=user_id
        )
        return cart
