from core.permissions import IsAuthenticatedPermission
from core.exceptions import Custom403Exception


class IsAuthenticatedActiveSellerUserPermission(IsAuthenticatedPermission):
    def has_permission(self, request, view):
        super().has_permission(request, view)
        if not request.user.groups.filter(name="Sale").exists():
            raise Custom403Exception
        return True
