from shop.models import Cart, CartItem
from shop.repositories import ProductRepository, CartRepository


class CartService:
    def __init__(self, *args, **kwargs):
        self.product_repository = ProductRepository()
        self.cart_repository = CartRepository()

    def add_product_to_cart_by_product_id_and_user_id(
        self, user_id: int, product_id: int
    ):
        cart, _ = self.cart_repository.create_get_or_create_cart_for_user_by_user_id(
            user_id=user_id
        )
        product_added = (
            self.cart_repository.add_product_to_cart_by_user_id_and_product_id(
                product_id=product_id, cart_id=cart.id
            )
        )
        if not product_added:
            return False
        return True

    def decrease_product_quantity_on_cart_by_user_id_and_product_id(
        self, user_id: int, product_id: int
    ):
        product_removed = self.cart_repository.decrease_product_quantity_from_cart_by_user_id_and_product_id(
            product_id=product_id, user_id=user_id
        )
        if not product_removed:
            return False
        return True
