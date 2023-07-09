from common.serializers.mixins import ExtendedModelSerializer
from users.models.profiles import UserPhotos


class PhotosShortSerializer(ExtendedModelSerializer):
    class Meta:
        model = UserPhotos
        fields = (
            'photo1',
            'photo2',
            'photo3',
            'photo4',
            'photo5',
            'photo6',
        )
