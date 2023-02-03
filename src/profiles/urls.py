from rest_framework.routers import DefaultRouter

from . import api

router = DefaultRouter()

router.register(r'account', api.UserQuePublicAPI, basename="account")
router.register(r'registration', api.CreateUserInTelegram, basename="users")
router.register(r'login', api.LoginUser, basename="login")
urlpatterns = router.urls
