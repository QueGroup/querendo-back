from .serializers import UserQueSerializer, UserQuePublicSerializer, UserListSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from .models import QueUser


class UserQuePublicAPI(ModelViewSet):
    """
    Output public user account
    """
    serializer_class = UserQuePublicSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return QueUser.objects.filter(id=self.request.user.id)


class UserQueAPI(ModelViewSet):
    """
    Output user info
    """
    serializer_class = UserQueSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return QueUser.objects.filter(telegram_id=self.request.user.telegram_id)


class UserListAPI(ModelViewSet):
    """
    Output list of users
    """
    queryset = QueUser.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
