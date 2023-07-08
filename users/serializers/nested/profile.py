from rest_framework import serializers

from users.models.profiles import Profile


# TODO: Добавить еще сериализатор, чтобы пользователь мог добавлять фотографии
#       Также добавить сериализатор для интересов
class ProfileShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'telegram_id',
            'gender',
            'age',
            'date_of_birth',
            'occupation',
            'interests',
            'description',
            'language',
            'country',
            'city',
            'longitude',
            'latitude',
        )


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'telegram_id',
            'gender',
            'age',
            'date_of_birth',
            'occupation',
            'interests',
            'description',
            'language',
            'country',
            'city',
            'longitude',
            'latitude',
        )
