from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema
)
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

from users.models.users import User
from users.serializers.api import (
    auth,
)


@extend_schema_view(
    post=extend_schema(summary="Регистрация пользователя в telegram", tags=["Аутентификация & Авторизация"])
)
class TelegramRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = auth.TelegramRegistration


@extend_schema_view(
    post=extend_schema(summary="Аутентификация пользователя через телеграм", tags=["Аутентификация & Авторизация"])
)
class TelegramTokenCreateView(TokenObtainPairView):
    serializer_class = auth.TelegramTokenCreateSerializer
