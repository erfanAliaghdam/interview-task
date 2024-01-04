from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from core.api.v1.serializers import LoginClientUserSerializer
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def login_client_user_view(request):
    """
    input data:
        {
            "email": "client@example.com",
            "password": "DefaultPassword"
        }
    """
    serializer = LoginClientUserSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {
                "status": "failed",
                "message": "Invalid input.",
                "data": {"errors": serializer.errors},
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    # check if can authenticate user
    user = authenticate(email=request.data["email"], password=request.data["password"])
    if not user:
        return Response(
            {
                "status": "failed",
                "message": "Invalid input.",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    # get or create token
    token, _ = Token.objects.get_or_create(user=user)
    # TODO: send notification
    return Response(
        {
            "status": "success",
            "message": "user token retrieved in successfully.",
            "data": {"token": token.key},
        },
        status=status.HTTP_200_OK,
    )
