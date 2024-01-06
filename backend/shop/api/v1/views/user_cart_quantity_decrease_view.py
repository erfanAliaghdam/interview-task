from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.response import Response
from shop.repositories import ProductRepository
from shop.services import CartService
from core.permissions import IsAuthenticatedPermission

product_repository = ProductRepository()
cart_service = CartService()


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticatedPermission])
def user_decrease_cart_quantity_view(request, slug: str):
    product = product_repository.get_product_by_slug(slug=slug)
    if not product:
        return Response(
            {"status": "failed", "message": "product not found."},
            status=status.HTTP_404_NOT_FOUND,
        )
    product_quantity_decreased = (
        cart_service.decrease_product_quantity_on_cart_by_user_id_and_product_id(
            user_id=request.user.id, product_id=product.id
        )
    )
    if not product_quantity_decreased:
        return Response(
            {"status": "failed", "message": "product not found."},
            status=status.HTTP_404_NOT_FOUND,
        )
    return Response(
        {
            "status": "success",
            "message": "product quantity decreased successfully.",
        },
        status=status.HTTP_200_OK,
    )
