from django.utils.text import slugify

from shop.repositories import ProductRepository


class ProductService:
    def __init__(self, *args, **kwargs):
        self.repository = ProductRepository()

    def slugify_product_by_id_and_title(
        self, title: str, product_id: int = None
    ) -> str:
        original_slug = slugify(title)
        product_existence = (
            self.repository.check_if_product_with_same_slug_exists_by_id_and_slug(
                product_id=product_id, slug=original_slug
            )
        )
        count = 1
        product_slug = original_slug
        while product_existence:
            # If a product with the same slug exists, append a count to the slug
            product_slug = f"{original_slug}-{count}"
            count += 1
            product_existence = (
                self.repository.check_if_product_with_same_slug_exists_by_id_and_slug(
                    product_id=product_id, slug=product_slug
                )
            )
        return product_slug
