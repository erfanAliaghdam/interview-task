import logging
from django.db import transaction
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.response import Response
from shop.repositories import CartRepository
from core.permissions import IsAuthenticatedPermission
from shop.services.order_service import OrderService

order_service = OrderService()
cart_repository = CartRepository()


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticatedPermission])
def user_make_order_view(request):
    # check cart items if not exists, return response
    cart_items = cart_repository.get_cart_items_by_user_id(user_id=request.user.id)

    if not cart_items:
        return Response(
            {"status": "failed", "message": "your cart is empty."},
            status=status.HTTP_412_PRECONDITION_FAILED,
        )

    # create order items based on cart items, then return response
    try:
        with transaction.atomic():
            order_service.place_order(user_id=request.user.id)
            cart_items.delete()
            return Response(
                {"status": "success", "message": "your order placed successfully."},
                status=status.HTTP_200_OK
            )
    except Exception as e:
        logging.error(e)
        response = {
            "status": "failed",
            "message": "Please try again later.",
        }
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

