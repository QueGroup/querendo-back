from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT

from common.views.mixins import ListViewSet
from users.models.users import User
from users.serializers.api import users as user_s


@extend_schema_view(
    get=extend_schema(summary="Профиль пользователя", tags=["Пользователи"]),
    put=extend_schema(summary="Изменить профиль пользователя", tags=["Пользователи"]),
    patch=extend_schema(summary="Изменить частично пользователя", tags=["Пользователи"]),
    delete=extend_schema(summary="Удалить профиль", tags=["Пользователи"])
)
class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return user_s.MeUpdateSerializer
        return user_s.MeListSerializer

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Профиль успешно удален"}, status=HTTP_204_NO_CONTENT)


@extend_schema_view(
    list=extend_schema(summary="Список пользователей Search", tags=["Словари"])
)
class UserListSearchView(ListViewSet):
    # TODO: Убрать из списка superusers
    queryset = User.objects.all()
    serializer_class = user_s.UserSearchListSerializer
