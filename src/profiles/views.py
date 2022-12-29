from rest_framework.viewsets import ModelViewSet

from .serializers import GetUserQueSerializer, GetUserQuePublicSerializer
from rest_framework import permissions
from .models import UserQue


class UserQuePublicView(ModelViewSet):
    """
    Output public user profile
    """
    queryset = UserQue.objects.all()
    serializer_class = GetUserQuePublicSerializer
    permission_classes = [permissions.AllowAny]


class UserQueView(ModelViewSet):
    """
    Output user info
    """
    serializer_class = GetUserQueSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserQue.objects.filter(id=self.request.user.id)
