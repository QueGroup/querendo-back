from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema
)
from rest_framework.permissions import (
    IsAuthenticated,
)

from common.permissions import (
    IsAdminOrReadOnly,
)
from common.views.mixins import (
    LCRUView,
    generics
)
from users.models.interests import (
    Interest
)
from users.serializers.api import (
    users as user_s,
    User,
)
from users.serializers.nested import (
    InterestUpdateSerializer
)


@extend_schema_view(
    post=extend_schema(summary="Создать интерес", tags=["Интересы"]),
    get=extend_schema(summary="Все интересы", tags=["Интересы"]),
)
class InterestView(
    LCRUView
):
    queryset = Interest.objects.all()
    serializer_class = InterestUpdateSerializer
    permission_classes = [IsAdminOrReadOnly]


@extend_schema_view(
    get=extend_schema(summary="Интересы пользователя", tags=["Интересы"]),
    put=extend_schema(summary="Изменить интересы пользователя", tags=["Интересы"]),
    patch=extend_schema(summary="Изменить частично интересы пользователя", tags=["Интересы"]),
)
class InterestAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return user_s.MeInterestUpdateSerializer
        return user_s.MeListSerializer
