from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from shop.api.v1.serializers import UserOrderListSerializer
from shop.repositories import OrderRepository
from core.permissions import IsAuthenticatedPermission

order_repository = OrderRepository()


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticatedPermission])
def user_order_list_view(request):
    paginator = PageNumberPagination()
    all_orders = order_repository.get_order_with_all_data_and_total_price_by_user_id(
        user_id=request.user.id
    )
    result_page = paginator.paginate_queryset(all_orders, request)
    serializer = UserOrderListSerializer(result_page, many=True)
    return Response(
        {
            "status": "success",
            "message": "user orders retrieved successfully.",
            "count": paginator.page.paginator.count,
            "next": paginator.get_next_link(),
            "previous": paginator.get_previous_link(),
            "data": serializer.data,
        },
        status=status.HTTP_200_OK,
    )
