from rest_framework import serializers
from .models import QueUser, Profile


class GetUserQueSerializer(serializers.ModelSerializer):
    """
    Output info about our user
    """
    avatar = serializers.ImageField(write_only=True)

    class Meta:
        model = QueUser
        exclude = (
            "password",
            "last_login",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
            "phone",
        )


class GetUserQuePublicSerializer(serializers.ModelSerializer):
    """
    Output public info about our user
    """
    avatar = serializers.ImageField(write_only=True)

    class Meta:
        model = QueUser
        exclude = (
            "email",
            "phone",
            "password",
            "last_login",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
        )


class GetUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
