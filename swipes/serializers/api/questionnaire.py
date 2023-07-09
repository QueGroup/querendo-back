from common.serializers.mixins import ExtendedModelSerializer
from users.models.users import User
from users.serializers.nested import (
    ProfileShortSerializer,
    PhotosShortSerializer
)


class QuestionnaireSerializer(ExtendedModelSerializer):
    profile = ProfileShortSerializer()
    photos = PhotosShortSerializer()

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'profile',
            'photos',
        )
