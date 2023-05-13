from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import generics

from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from users.models.users import User
from users.serializers.api import users as user_s


@extend_schema_view(
    post=extend_schema(summary='Регистрация пользователя', tags=['Аутентификация & Авторизация'])
)
class RegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = user_s.RegistrationSerializer


@extend_schema_view(

    post=extend_schema(
        summary="Смена пароля",
        tags=['Аутентификация & Авторизация'], )
)
class ChangePasswordView(APIView):

    def get_serializer(self, *args, **kwargs):
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
    get=extend_schema(summary="Профиль пользователя", tags=['Пользователи']),
    patch=extend_schema(summary="Изменить частично пользователя", tags=['Пользователи'])
)
class MyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    http_method_names = ("get", "patch")

    def get_serializer_class(self):
        if self.request.method == "GET":
            return user_s.MeListSerializer
        return user_s.MeUpdateSerializer

    def get_object(self):
        return self.request.user
