from rest_framework.viewsets import ModelViewSet

from .serializers import GetUserQueSerializer, GetUserQuePublicSerializer, GetUserProfileSerializer
from rest_framework import permissions
from .models import QueUser, Profile


class UserQuePublicAPI(ModelViewSet):
    """
    Output public user account
    """
    queryset = QueUser.objects.all()
    serializer_class = GetUserQuePublicSerializer
    permission_classes = [permissions.AllowAny]


class UserQueAPI(ModelViewSet):
    """
    Output user info
    """
    serializer_class = GetUserQueSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return QueUser.objects.filter(id=self.request.user.id)


class ProfilePublicAPI(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = GetUserProfileSerializer
    permission_classes = [permissions.AllowAny]


class ProfileAPI(ModelViewSet):
    serializer_class = GetUserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.filter(id=self.request.user.id)
