from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([])
def test_view(request):
    if not request.user.is_authenticated:
        return Response({"status": "failed"})
    return Response({"status": "success"})
