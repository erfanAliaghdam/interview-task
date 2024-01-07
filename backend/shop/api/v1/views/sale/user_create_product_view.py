from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.response import Response
from shop.api.v1.serializers import ProductCreateSerializer
from shop.repositories import ProductRepository
from core.permissions.seller import IsAuthenticatedActiveSellerUserPermission

product_repository = ProductRepository()


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticatedActiveSellerUserPermission])
def product_create_view(request):
    serializer = ProductCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {
                "status": "failed",
                "message": "product creation failed.",
                "data": {"errors": serializer.errors},
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    product_repository.create_product(
        title=serializer.validated_data.get("title"),
        description=serializer.validated_data.get("description"),
        price=serializer.validated_data.get("price"),
        stock=serializer.validated_data.get("stock"),
    )
    return Response(
        {
            "status": "success",
            "message": "product created successfully.",
        },
        status=status.HTTP_200_OK,
    )
