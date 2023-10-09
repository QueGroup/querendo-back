from common.serializers.mixins import ExtendedModelSerializer
from users.models import BrandBook
from users.models.photos import UserPhotos


class PhotosShortSerializer(ExtendedModelSerializer):
    class Meta:
        model = UserPhotos
        fields = (
            'photo1',
            'photo2',
            'photo3',
            'photo4',
            'photo5',
        )


class TelegramPhotoSerializer(ExtendedModelSerializer):
    class Meta:
        model = UserPhotos
        fields = (
            'photo1',
            'photo2',
            'photo3',
            'photo4',
            'photo5',
            'file_id1',
            'file_id2',
            'file_id3',
            'file_id4',
            'file_id5',
        )


class TelegramPhotoShortSerializer(ExtendedModelSerializer):
    class Meta:
        model = UserPhotos
        fields = (
            'file_id1',
            'file_id2',
            'file_id3',
            'file_id4',
            'file_id5',
        )


class BrandBookSerializer(ExtendedModelSerializer):
    class Meta:
        model = BrandBook
        fields = (
            "id",
            "photo"
        )
