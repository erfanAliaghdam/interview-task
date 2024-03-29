from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.response import Response
from shop.api.v1.serializers import UserCartSerializer
from shop.repositories import CartRepository
from core.permissions.client import IsAuthenticatedActiveClientUserPermission

cart_repository = CartRepository()


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticatedActiveClientUserPermission])
def user_cart_list_view(request):
    cart = cart_repository.get_cart_with_all_data_and_total_price_by_user_id(
        user_id=request.user.id
    )
    serializer = UserCartSerializer(cart)
    return Response(
        {
            "status": "success",
            "message": "user cart retrieved successfully.",
            "data": serializer.data,
        },
        status=status.HTTP_200_OK,
    )
