from core.exceptions import Custom401Exception, Custom403Exception
from rest_framework.permissions import BasePermission


class IsAuthenticatedPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise Custom401Exception
        if not request.user.is_active:
            raise Custom403Exception
        return True
