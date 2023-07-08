from collections import OrderedDict
from typing import Union

from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from users.models.users import User
from users.serializers.nested.profile import ProfileShortSerializer, ProfileUpdateSerializer


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'email',
            'password',
            'username',
        )

    @staticmethod
    def validate_email(value: str):
        email = value.lower()
        if User.objects.filter(email=email).exists():
            raise ParseError(
                "Пользователь с такой почтой уже зарегистрирован"
            )
        return email

    @staticmethod
    def validate_password(value: str):
        validate_password(value)
        return value

    def create(self, validated_data: dict):
        user = User.objects.create_user(**validated_data)
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'old_password',
            'new_password',
        )

    def validate(self, attrs: dict):
        user = self.instance
        old_password = attrs.pop('old_password')
        if not user.check_password(old_password):
            raise ParseError(
                "Проверьте правильность введенного пароля"
            )
        return attrs

    @staticmethod
    def validate_new_password(value: str):
        validate_password(value)
        return value

    def update(self, instance: User, validated_data: dict):
        password = validated_data.pop('new_password')
        instance.set_password(password)
        instance.save()
        return instance


class MeListSerializer(serializers.ModelSerializer):
    profile = ProfileShortSerializer()

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'username',
            'profile',
            'date_joined',
        )


class MeUpdateSerializer(serializers.ModelSerializer):
    profile = ProfileUpdateSerializer()

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'username',
            'profile',
        )

    def update(self, instance: User, validated_data: dict):
        profile_data = validated_data.pop('profile') if 'profile' in validated_data else None

        with transaction.atomic():
            instance = super().update(instance, validated_data)
            if profile_data:
                self._update_profile(instance.profile, profile_data)

        return instance

    @staticmethod
    def _update_profile(profile: User, data: Union[OrderedDict, dict]):
        profile_serializer = ProfileUpdateSerializer(
            instance=profile, data=data, partial=True
        )
        profile_serializer.is_valid(raise_exception=True)
        profile_serializer.save()


class UserSearchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'full_name',
        )
