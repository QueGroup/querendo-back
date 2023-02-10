from rest_framework.routers import DefaultRouter

from . import api

router = DefaultRouter()

router.register(r'account', api.UserQuePublicAPI, basename="account")
router.register(r'photos', api.AddProfilePhotos, basename="photos")

urlpatterns = router.urls
