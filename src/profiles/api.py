from django.views.generic import CreateView

from .serializers import UserQueSerializer, UserQuePublicSerializer, UserListSerializer, UserSerializer
from .serializers import VerifyAccountSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from .models import QueUser
from .tasks import check_age
from rest_framework.views import APIView
from rest_framework.response import Response
from .emails import send_otp_to_email


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
        return QueUser.objects.filter(id=self.request.user.id)


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


# email reg

class RegisterAPI(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            data = request.data
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                send_otp_to_email(serializer.data['email'])
                return Response({
                    'status': 200,
                    'message': "You has been registered, check email to finalize register",
                    'data': serializer.data
                })
            return Response({
                'status': 400,
                'message': f"Smt went wrong",
                'data': serializer.data
            })
        except Exception as error:
            print(error)

class VerifyOTP(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        try:
            data = request.data
            serializer = VerifyAccountSerializer(data=data)
            if serializer.is_valid():
                email = serializer.data['email']
                otp = serializer.data['otp']

                user = QueUser.objects.filter(email=email).first()
                if user.email == '':
                    return Response({
                        'status': 400,
                        'message': f"Invalid email",
                        'data': serializer.data
                    })
                if not user.otp == otp:
                    return Response({
                        'status': 400,
                        'message': f"wrong otp",
                        'data': serializer.data
                    })

                user.is_verified = True
                user.save()

                return Response({
                    'status': 200,
                    'message': "Your account has been verified",
                    'data': serializer.data
                })

            return Response({
                'status': 400,
                'message': f"Smt went wrong",
                'data': serializer.data
            })
        except Exception as error:
            print(error)
