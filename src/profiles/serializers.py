from django.contrib.auth.hashers import make_password
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from .models import QueUser, UserPhoto


class UserQueSerializer(serializers.ModelSerializer):
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


class UserQuePublicSerializer(serializers.ModelSerializer):
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


class CreateUser(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = QueUser
        fields = ['telegram_id', 'username', 'password', 'phone', 'birthday']



class ImageForm(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = UserPhoto
        fields = ('image',)
