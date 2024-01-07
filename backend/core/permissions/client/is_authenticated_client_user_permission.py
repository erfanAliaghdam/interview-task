from core.permissions import IsAuthenticatedPermission
from core.exceptions import Custom403Exception


class IsAuthenticatedActiveClientUserPermission(IsAuthenticatedPermission):
    def has_permission(self, request, view):
        super().has_permission(request, view)
        if not request.user.groups.filter(name="Client").exists():
            raise Custom403Exception
        return True
