from django.urls import path
from rest_framework.routers import DefaultRouter

from . import api

app_name = 'profiles'

router = DefaultRouter()

router.register(r'account', api.UserQuePublicAPI, basename='account')
router.register(r'verify', api.VerifyOTP, basename='verify')
router.register(r'register', api.RegisterAPI, basename='register')
router.register(r'login', api.LoginAPI, basename='login')
router.register(r'reset-password', api.ResetPasswordRequestAPI, basename='reset-password')
router.register(r'confirm-otp', api.ResetPasswordAPI, basename='confirm-otp')
router.register(r'confirm-password', api.ResetPasswordConfirmAPI, basename='confirm-password')
urlpatterns = [
    path('users/telegram/<str:telegram_id>/', api.UserListAPI.as_view({'get': 'retrieve', 'put': 'put'}),
         name='user-detail'),
    path('users/email/<str:email>/', api.UserListAPI.as_view({'get': 'retrieve', 'put': 'put'}), name='user-detail'),
]
router.register(r'register-with-tg', api.TelegramUserViewSet, basename='reg-with-tg')
router.register(r'user-save-photo', api.UserPhotosViewSet, basename='user-save-photo')
urlpatterns += router.urls
