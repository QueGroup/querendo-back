from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
)
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.response import (
    Response,
)
from rest_framework.status import (
    HTTP_204_NO_CONTENT,
)

from common.views.mixins import (
    LRUDAPIView,
)
from users.models.users import (
    User,
)
from users.serializers.api import (
    users as user_s
)


@extend_schema_view(
    list=extend_schema(summary="Список пользователей", tags=["Пользователи"]),
    get=extend_schema(summary="Пользователь", tags=["Пользователи"]),
    put=extend_schema(summary="Изменить пользователя", tags=["Пользователи"]),
    patch=extend_schema(summary="Изменить частично пользователя", tags=["Пользователи"]),
    delete=extend_schema(summary="Удалить пользователя", tags=["Пользователи"])
)
class UserAPIView(LRUDAPIView):
    queryset = User.objects.all()
    serializer_class = user_s.UserSearchListSerializer
    permission_classes = [IsAuthenticated]
    # parser_classes = [MultiPartParser, FormParser]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return user_s.MeUpdateSerializer
        return user_s.MeListSerializer

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        if self.request.method == "DELETE":
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"message": "Профиль успешно удален"}, status=HTTP_204_NO_CONTENT)
        return super().destroy(request, *args, **kwargs)
