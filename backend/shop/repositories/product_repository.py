from _decimal import Decimal
from typing import List
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

    def get_products_by_id_list(self, product_ids=List[int]):
        return Product.objects.filter(id__in=product_ids)

    def _filter_by_search_term(self, queryset, search_term: str):
        return queryset.filter(title__contains=search_term)

    def _filter_by_in_stock(self, queryset, in_stock: bool):
        if not in_stock:
            return queryset.filter(stock=0)
        return queryset.filter(stock__gt=0)

    def get_all_products_by_filters(
        self, search_term: str = None, in_stock: bool = None
    ):
        all_products = self.get_all_products()
        if search_term:
            all_products = self._filter_by_search_term(
                queryset=all_products, search_term=search_term
            )
        if in_stock is not None:
            all_products = self._filter_by_in_stock(
                queryset=all_products, in_stock=in_stock
            )
        return all_products

    def create_product(self, title: str, description: str, price: Decimal, stock: int):
        product = Product.objects.create(
            title=title, description=description, price=price, stock=stock
        )
        return product
