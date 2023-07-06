from rest_framework import serializers

from users.models.profiles import Profile


class ProfileShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'telegram_id',
            'gender',
            'age',
        )


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'telegram_id',
            'gender',
            'age',
        )
