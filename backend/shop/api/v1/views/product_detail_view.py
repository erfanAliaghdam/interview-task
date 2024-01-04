from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.response import Response
from shop.api.v1.serializers import ProductDetailSerializer
from shop.repositories import ProductRepository
from core.permissions import IsAuthenticatedPermission


product_repository = ProductRepository()


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticatedPermission])
def product_detail_view(request, slug: str):
    product = product_repository.get_product_by_slug(slug=slug)
    if not product:
        return Response(
            {"status": "failed", "message": "product not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = ProductDetailSerializer(product)
    return Response(
        {
            "status": "success",
            "message": "product retrieved successfully.",
            "data": serializer.data,
        },
        status=status.HTTP_200_OK,
    )
