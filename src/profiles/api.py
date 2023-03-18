from django.contrib.auth import authenticate, login
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView
from rest_framework import permissions, status, viewsets
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey

from .emails import send_otp_to_email, generate_reset_password_otp, send_reset_password_otp_to_email
from .models import QueUser, UserPhotos
from .serializers import UserQuePublicSerializer, UserSerializer, UserLoginSerializer, \
    ResetPasswordSerializer, ResetPasswordRequestSerializer, ConfirmOTPSerializer, UserListSerializer, \
    TelegramUserSerializer, UserPhotosSerializer
from .serializers import VerifyAccountSerializer
from .tasks import check_age


class UserQuePublicAPI(viewsets.ModelViewSet):
    """
    Output public user account
    """
    serializer_class = UserQuePublicSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly | HasAPIKey]
    queryset = QueUser.objects.all()
    lookup_field = 'telegram_id'


class UserListAPI(viewsets.ModelViewSet):
    queryset = QueUser.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        pk = self.kwargs.get('pk')
        if pk is not None:
            obj = get_object_or_404(queryset, pk=pk)
            return obj

        telegram_id = self.kwargs.get('telegram_id')
        if telegram_id is not None:
            obj = get_object_or_404(queryset, telegram_id=telegram_id)
            return obj

        email = self.kwargs.get('email', None)
        if email is not None:
            obj = get_object_or_404(queryset, email=email)
            return obj

        raise Http404

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        # Get the `telegram_id` and `email` values from the URL kwargs
        telegram_id = kwargs.get('telegram_id')
        email = kwargs.get('email')

        # Ensure that at least one of `telegram_id` or `email` is provided
        if telegram_id is None and email is None:
            return Response({'error': 'Either telegram_id or email must be provided.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Get the user object based on the provided `telegram_id` or `email`
        queryset = self.get_queryset()
        if telegram_id is not None:
            user = get_object_or_404(queryset, telegram_id=telegram_id)
        else:
            user = get_object_or_404(queryset, email=email)

        # Update the user object with the new data from the request
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Return the updated user object as serialized data
        return Response(serializer.data)


class TestCelery(CreateView):
    """
    Тестовый класс celery
    """

    def form_valid(self, form):
        form.save()
        check_age.delay(form.instance.email)
        return super().form_valid(form)


class RegisterAPI(viewsets.ModelViewSet):
    """
    Registration by email
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer
    queryset = QueUser.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            send_otp_to_email(serializer.data['email'])

            return Response({
                'status': status.HTTP_200_OK,
                'message': 'You have been registered, check your email to finalize registration',
                'data': serializer.data
            })
        except Exception as error:
            print(error)
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Something went wrong'
            })


class VerifyOTP(viewsets.ModelViewSet):
    """
    The class with which the user confirms his mail
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = VerifyAccountSerializer
    queryset = QueUser.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']

            user = QueUser.objects.filter(email=email).first()
            if not user:
                return Response({
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Invalid email',
                    'data': serializer.data
                })
            if not user.otp == otp:
                return Response({
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Wrong otp',
                    'data': serializer.data
                })

            user.is_verified = True
            user.save()

            return Response({
                'status': status.HTTP_200_OK,
                'message': 'Your account has been verified',
                'data': serializer.data
            })
        except Exception as error:
            print(error)
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Something went wrong'
            })


class LoginAPI(viewsets.ModelViewSet):
    """
    User login API
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = UserLoginSerializer
    queryset = QueUser.objects.all()

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_active:
                # Login the user and return a success response
                login(request, user)
                return Response({
                    'status': status.HTTP_200_OK,
                    'message': 'Login successful',
                    'data': {
                        'user_id': user.id,
                        'email': user.email,
                    }
                })
            else:
                # User is not active, return an error response
                return Response({
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'User account is not active',
                })
        else:
            # Email and/or password are incorrect, return an error response
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Invalid email and/or password',
            })


class ResetPasswordRequestAPI(viewsets.ModelViewSet):
    """
    Class for handling password reset requests by email
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = ResetPasswordRequestSerializer
    queryset = QueUser.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data['email']

            user = QueUser.objects.filter(email=email).first()
            if not user:
                return Response({
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Invalid email',
                    'data': serializer.data
                })
            reset_password_otp = generate_reset_password_otp()
            user.reset_password_otp = reset_password_otp
            user.save()
            send_reset_password_otp_to_email(email, reset_password_otp)

            return Response({
                'status': status.HTTP_200_OK,
                'message': 'Reset password OTP sent to your email',
                'data': serializer.data
            })
        except Exception as error:
            print(error)
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Something went wrong'
            })


class ResetPasswordAPI(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = ConfirmOTPSerializer
    queryset = QueUser.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']

            user = QueUser.objects.filter(email=email).first()
            if not user.reset_password_otp == otp:
                return Response({
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Wrong OTP',
                    'data': serializer.data
                })

            return Response({
                'status': status.HTTP_200_OK,
                'message': 'OTP is correct',
                'data': serializer.data
            })
        except Exception as error:
            print(error)
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Wrong',
            })


class ResetPasswordConfirmAPI(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = ResetPasswordSerializer
    queryset = QueUser.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data['email']
            new_password = serializer.validated_data['new_password']

            user = QueUser.objects.filter(email=email).first()

            if 8 < len(new_password) > 128:
                return Response({
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'You have entered either very short passwords or too long',
                    'data': serializer.data
                })

            user.set_password(new_password)
            user.reset_password_otp = None
            user.save()

            return Response({
                'status': status.HTTP_200_OK,
                'message': 'Password reset successful',
                'data': serializer.data
            })
        except Exception as error:
            print(error)
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Wrong',
            })


class TelegramUserViewSet(viewsets.ModelViewSet):
    serializer_class = TelegramUserSerializer
    queryset = QueUser.objects.all()
    permission_classes = [permissions.AllowAny]
    parser_classes = [JSONParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        response_data = {
            "message": "User created successfully.",
            "user_id": instance.pk
        }
        return Response(response_data, status=201)


class UserPhotosViewSet(viewsets.ModelViewSet):
    serializer_class = UserPhotosSerializer
    queryset = UserPhotos.objects.all()
    permission_classes = [permissions.AllowAny]
    parser_classes = (MultiPartParser, FormParser)

    def get_parsers(self):
        if getattr(self, 'swagger_fake_view', False):
            return []
        return super().get_parsers()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        response_data = {
            "message": "User photo(s) created successfully.",
            "user_id": instance.user_account_id.pk,
            "photo1": instance.photo1.url if instance.photo1 else None,
            "photo2": instance.photo2.url if instance.photo2 else None,
            "photo3": instance.photo3.url if instance.photo3 else None,
            "photo4": instance.photo4.url if instance.photo4 else None,
            "photo5": instance.photo5.url if instance.photo5 else None,
            "photo6": instance.photo6.url if instance.photo6 else None,
        }
        return Response(response_data, status=201)
