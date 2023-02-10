from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, status
from .models import QueUser, UserPhoto
from .serializers import UserQueSerializer, UserQuePublicSerializer, ImageForm


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
class AddProfilePhotos(ModelViewSet):
    queryset = UserPhoto.objects.all()
    serializer_class = ImageForm
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        photos = {}
        for i in range(1, 7):
            try:
                photos[f'photo{i}'] = request.data.get(f'photo{i}')
            except KeyError:
                photos[f'photo{i}'] = None

        photo_set = UserPhoto.objects.create(
            user_account_id=request.data.get('user_account_id'),
            photo1=request.data.get('photo1'),
            photo2=request.data.get('photo2'),
            photo3=request.data.get('photo3'),
            photo4=request.data.get('photo4'),
            photo5=request.data.get('photo5'),
            photo6=request.data.get('photo6')
        )
        if photo_set:
            return Response(status=status.HTTP_200_OK)
        return Response({'error': 'Something error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
