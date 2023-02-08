from rest_framework.routers import DefaultRouter

from . import api

router = DefaultRouter()

router.register(r'account', api.UserQuePublicAPI, basename="account")
urlpatterns = router.urls
