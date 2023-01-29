from rest_framework.routers import DefaultRouter

from . import api

router = DefaultRouter()

router.register(r'account', api.UserQueAPI, basename="account")
router.register(r'profile', api.ProfilePublicAPI, basename="profile")

urlpatterns = router.urls
