from django.views.generic import CreateView
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from .models import QueUser
from .serializers import UserQueSerializer, UserQuePublicSerializer
from .tasks import check_age


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


class TestCelery(CreateView):
    """
    Тестовый класс для celery
    """

    def form_valid(self, form):
        form.save()
        # С помощью delay мы используем celery
        check_age.delay(form.instance.email)
        return super().form_valid(form)
