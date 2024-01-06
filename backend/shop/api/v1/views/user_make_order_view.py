from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.response import Response
from core.permissions import IsAuthenticatedPermission
from shop.services.order_service import OrderService

order_service = OrderService()

#     NOTE:
#     I could implement this part with higher performance,
#     but due to using the service-repository pattern,
#     the implementation priority was to preserve the code structure.


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticatedPermission])
def user_make_order_view(request):
    # create order items based on cart items, then return response
    order_service.place_order(user_id=request.user.id)
    return Response(
        {"status": "success", "message": "your order placed successfully."},
        status=status.HTTP_200_OK,
    )
