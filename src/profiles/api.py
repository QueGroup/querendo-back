from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, status
from .models import QueUser
from .serializers import UserQueSerializer, UserQuePublicSerializer, TelegramUsersList


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


class CreateUserInTelegram(ModelViewSet):
    """
    Login in Telegram
    """
    queryset = QueUser.objects.all()
    serializer_class = TelegramUsersList
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        user = QueUser.objects.create(
            username=request.data.get('username'),
            password=make_password(request.data.get('password')),
            telegram_id=request.data.get('telegram_id'),
            gender=request.data.get('gender'),
            email=request.data.get('email'),
            birthday=request.data.get('birthday'),
            phone=request.data.get('phone')

        )
        if user:
            return Response(status=status.HTTP_200_OK)
        return Response({'error': 'Something error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginUser(ModelViewSet):
    queryset = QueUser.objects.all()
    serializer_class = TelegramUsersList
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            return Response(status=status.HTTP_200_OK)
        return Response({'error': 'Invalid login credentials'}, status=status.HTTP_401_UNAUTHORIZED)
