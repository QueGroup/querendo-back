from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from matches.models import Matches
# from matches.serializers.api import MatchesSerializer

class MatchesSerializer:
    ...

@extend_schema_view(
    get=extend_schema(summary='Список мэтчей', tags=['Мэтчи']),
    post=extend_schema(summary='Создать мэтч', tags=['Мэтчи']),
)
class MatchesView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MatchesSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Matches.objects.filter(user1=user) | Matches.objects.filter(user2=user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user1=self.request.user)

    @staticmethod
    def send_match_notification(liked_client, target_client, topic='Match!'):
        ...
