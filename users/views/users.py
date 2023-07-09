from typing import Any

from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from common.views.mixins import ListViewSet
from users.models.users import User
from users.serializers.api import users as user_s


@extend_schema_view(
    post=extend_schema(summary="Регистрация пользователя", tags=["Аутентификация & Авторизация"])
)
class RegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = user_s.RegistrationSerializer


@extend_schema_view(
    post=extend_schema(summary="Регистрация пользователя в telegram", tags=["Аутентификация & Авторизация"])
)
class TelegramRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = user_s.TelegramRegistration


@extend_schema_view(

    post=extend_schema(
        summary="Смена пароля",
        tags=["Аутентификация & Авторизация"], )
)
class ChangePasswordView(APIView):

    def get_serializer(self, *args: Any, **kwargs: Any):
        return user_s.ChangePasswordSerializer(*args, **kwargs)

    def post(self, request: Request) -> Response:
        user = request.user
        serializer = self.get_serializer(
            instance=user, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=HTTP_204_NO_CONTENT)


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
