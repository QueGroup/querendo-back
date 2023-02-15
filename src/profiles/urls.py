from rest_framework.routers import DefaultRouter
from . import api
from django.urls import path
from .api import RegisterAPI, VerifyOTP
app_name = 'profiles'
urlpatterns = [
    path("register/", RegisterAPI.as_view()),
    path("verify/", VerifyOTP.as_view()),
]

router = DefaultRouter()

router.register(r'account', api.UserQuePublicAPI, basename='account')
router.register(r'users', api.UserListAPI, basename='users')
