from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status, generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from common.permissions import IsAdminOrReadOnly
from common.views.mixins import LCRUView
from users.models import BrandBook, Photo
from users.serializers.nested import (
    BrandBookSerializer,
    PhotosShortSerializer
)


@extend_schema_view(
    post=extend_schema(summary="Загрузить страницу брендбука", tags=["Брендбук"]),
    get=extend_schema(summary="Все страницы брендбука", tags=["Брендбук"])
)
class BrandBookView(
    LCRUView
):
    queryset = BrandBook.objects.all()
    serializer_class = BrandBookSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]


class ProfilePhoto(
    generics.UpdateAPIView
):
    serializer_class = PhotosShortSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Photo.objects.filter(user=self.request.user).first()

    @extend_schema(
        summary="Загрузить фотографию", tags=["Пользователи"]
    )
    def patch(self, request: Request, *args, **kwargs) -> Response:
        instance = self.get_queryset()
        serializer = self.get_serializer(instance=instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
