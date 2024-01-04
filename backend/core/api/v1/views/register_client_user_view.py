import logging

from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from core.services import RegisterUserService
from core.api.v1.serializers import RegisterClientUserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)


user_service = RegisterUserService()


@api_view(["POST"])
@permission_classes([])
@authentication_classes([])
def register_client_user_view(request):
    """
    input data:
        {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            "password": "DefaultPassword"
        }
    """
    serializer = RegisterClientUserSerializer(data=request.data)
    if not serializer.is_valid():
        response = {
            "status": "failed",
            "message": "client registration failed.",
            "data": {"errors": serializer.errors},
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    # we can return some config data for caching,
    # this practice can prevent extra requests
    try:
        with transaction.atomic():
            user = user_service.register_client_user(
                first_name=serializer.validated_data.get("first_name"),
                last_name=serializer.validated_data.get("last_name"),
                email=serializer.validated_data.get("email"),
                password=serializer.validated_data.get("password"),
            )
            token, _ = Token.objects.get_or_create(user=user)
            response = {
                "status": "success",
                "message": "client registered successfully.",
                "data": {"token": token.key},
            }
            return Response(response, status=status.HTTP_200_OK)
    except Exception as e:
        logging.error(e)
        response = {
            "status": "failed",
            "message": "Please try again later.",
        }
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
