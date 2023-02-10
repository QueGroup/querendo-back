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
    # image = serializers.ImageField()

    class Meta:
        model = UserPhoto
        fields = ['user_account_id', 'photo1', 'photo2', 'photo3', 'photo4', 'photo5', 'photo6']

    def create(self, validated_data):
        user = QueUser.objects.create(
            user_account_id=validated_data['user_account_id'],
            photo1=validated_data['photo1'],
            photo2=validated_data['photo2'],
            photo3=validated_data['photo3'],
            photo4=validated_data['photo4'],
            photo5=validated_data['photo5'],
            photo6=validated_data['photo6'],
        )
        return user

