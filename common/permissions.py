from rest_framework.permissions import (
    BasePermission,
)
from rest_framework.request import (
    Request,
)
from rest_framework.views import (
    APIView,
)


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request: Request, view: APIView):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True
        return request.user and request.user.is_superuser
