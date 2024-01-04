from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from shop.api.v1.serializers import ProductListSerializer
from shop.repositories import ProductRepository
from core.permissions import IsAuthenticatedPermission


product_repository = ProductRepository()


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticatedPermission])
def product_list_view(request):
    paginator = PageNumberPagination()
    products = product_repository.get_all_products().order_by("-created_at")
    result_page = paginator.paginate_queryset(products, request)

    serializer = ProductListSerializer(result_page, many=True)
    return Response(
        {
            "status": "success",
            "message": "product list retrieved successfully.",
            "count": paginator.page.paginator.count,
            "next": paginator.get_next_link(),
            "previous": paginator.get_previous_link(),
            "data": serializer.data,
        },
        status=status.HTTP_200_OK,
    )
