from django.db.models.expressions import RawSQL
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from users.models.users import User
from swipes.serializers.api import QuestionnaireSerializer


@extend_schema_view(
    get=extend_schema(summary='Свайпы', tags=['Просмотр анкет'])
)
class QuestionnairesListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = QuestionnaireSerializer

    # filter_backends = (filters.DjangoFilterBackend,)
    # filterset_class = ClientFilter

    def get_queryset(self):
        max_distance = self.request.query_params.get('distance')
        if max_distance is None:
            return User.objects.all()
        else:
            return self.get_clients_within_distance(float(max_distance))

    def get_clients_within_distance(self, max_distance):
        origin_lat = self.request.user.latitude
        origin_long = self.request.user.longitude
        gcd = "6371 * acos(least(greatest(\
        cos(radians(%s)) * cos(radians(latitude)) \
        * cos(radians(longitude) - radians(%s)) + \
        sin(radians(%s)) * sin(radians(latitude)) \
        , -1), 1))"
        distance_raw_sql = RawSQL(gcd, (origin_lat, origin_long, origin_lat))
        return User.objects.all().annotate(distance=distance_raw_sql).filter(distance__lt=max_distance)
