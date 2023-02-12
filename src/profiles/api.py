from django.views.generic import CreateView

from .serializers import UserQueSerializer, UserQuePublicSerializer, UserListSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from .models import QueUser
from .tasks import check_age


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

    def get_queryset(self):
        return QueUser.objects.filter(id=self.request.user.id)


class TestCelery(CreateView):
    """
    Тестовый класс для celery
    """

    def form_valid(self, form):
        form.save()
        check_age.delay(form.instance.email)
        return super().form_valid(form)
