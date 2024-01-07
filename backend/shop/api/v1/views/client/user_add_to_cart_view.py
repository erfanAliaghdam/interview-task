from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.response import Response
from shop.repositories import ProductRepository, CartRepository
from shop.services import CartService
from core.permissions.client import IsAuthenticatedActiveClientUserPermission

product_repository = ProductRepository()
cart_service = CartService()
cart_repository = CartRepository()


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticatedActiveClientUserPermission])
def user_add_to_cart_view(request, slug: str):
    # check if product exists or not
    product = product_repository.get_product_by_slug(slug=slug)
    if not product:
        return Response(
            {"status": "failed", "message": "product not found."},
            status=status.HTTP_404_NOT_FOUND,
        )
    if product.stock == 0:
        return Response(
            {"status": "failed", "message": "product is out of stock."},
            status=status.HTTP_412_PRECONDITION_FAILED,
        )

    added_to_cart = cart_service.add_product_to_cart_by_product_id_and_user_id(
        user_id=request.user.id, product_id=product.id
    )
    if not added_to_cart:
        return Response(
            {"status": "failed", "message": "product is out of stock."},
            status=status.HTTP_412_PRECONDITION_FAILED,
        )

    return Response(
        {
            "status": "success",
            "message": "product added to user cart successfully.",
        },
        status=status.HTTP_200_OK,
    )
