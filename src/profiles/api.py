from .serializers import UserQueSerializer, UserQuePublicSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from .models import QueUser


class UserQuePublicAPI(ModelViewSet):
    """
    Output public user account
    """
    queryset = QueUser.objects.all()
    serializer_class = UserQuePublicSerializer
    permission_classes = [permissions.AllowAny]


class UserQueAPI(ModelViewSet):
    """
    Output user info
    """
    serializer_class = UserQueSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return QueUser.objects.filter(id=self.request.user.id)
