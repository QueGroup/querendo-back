from typing import Any

from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from users.serializers.api import auth


@extend_schema_view(

    post=extend_schema(
        summary="Смена пароля",
        tags=["Аутентификация & Авторизация"], )
)
class ChangePasswordView(APIView):

    def get_serializer(self, *args: Any, **kwargs: Any):
        return auth.ChangePasswordSerializer(*args, **kwargs)

    def post(self, request: Request) -> Response:
        user = request.user
        serializer = self.get_serializer(
            instance=user, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=HTTP_204_NO_CONTENT)
