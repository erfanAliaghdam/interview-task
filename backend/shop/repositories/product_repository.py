from shop.models import Product


class ProductRepository:
    def check_if_product_with_same_slug_exists_by_id_and_slug(
        self, slug: str, product_id: int = None
    ):
        if product_id is None:
            return Product.objects.filter(slug=slug).exists()
        return Product.objects.filter(slug=slug).exclude(id=product_id).exists()

    def get_all_products(self):
        return Product.objects.all()

    def get_product_by_slug(self, slug: str):
        return Product.objects.filter(slug=slug).first()
