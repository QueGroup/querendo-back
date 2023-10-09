from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.parsers import MultiPartParser, FormParser

from common.permissions import IsAdminOrReadOnly
from common.views.mixins import LCRUView
from users.models import BrandBook
from users.serializers.nested import BrandBookSerializer


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
