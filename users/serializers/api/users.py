from collections import (
    OrderedDict,
)
from typing import (
    Union,
)

from django.db import (
    transaction,
)

from common.serializers.mixins import (
    ExtendedModelSerializer,
)
from users.models.users import (
    User,
)
from users.serializers.nested import (
    ProfileUpdateSerializer,
    ProfileShortSerializer,
    UserFilterShortSerializer,
    ProfileInterestUpdateSerializer,
    PhotoSerializer,
)


class MeListSerializer(ExtendedModelSerializer):
    profile = ProfileShortSerializer()
    photos = PhotoSerializer()
    filters = UserFilterShortSerializer()

    # interests = InterestSerializer()

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'username',
            'date_joined',
            'profile',
            'photos',
            'filters',
        )


class MeUpdateSerializer(ExtendedModelSerializer):
    photos = PhotoSerializer()
    filters = UserFilterShortSerializer()
    profile = ProfileUpdateSerializer()

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'phone_number',
            'telegram_id',
            'username',
            'profile',
            'photos',
            'filters',
        )

    def update(self, instance: User, validated_data: dict):
        photos_data = validated_data.pop('photos', None)
        filters_data = validated_data.pop('filters', None)
        profile_data = validated_data.pop('profile', None)

        with transaction.atomic():
            instance = super().update(instance, validated_data)
            if photos_data:
                self._update_photos(instance.photos, photos_data)
            if filters_data:
                self._update_filters(instance.filters, filters_data)
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

    @staticmethod
    def _update_photos(photos, data: Union[OrderedDict, dict]):
        photos_serializer = PhotoSerializer(
            instance=photos, data=data, partial=True
        )
        photos_serializer.is_valid(raise_exception=True)
        photos_serializer.save()

    @staticmethod
    def _update_filters(filters, data: Union[OrderedDict, dict]):
        filters_serializer = UserFilterShortSerializer(
            instance=filters, data=data, partial=True
        )
        filters_serializer.is_valid(raise_exception=True)
        filters_serializer.save()


class MeInterestUpdateSerializer(ExtendedModelSerializer):
    profile = ProfileInterestUpdateSerializer()

    class Meta:
        model = User
        fields = (
            'id',
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
        profile_serializer = ProfileInterestUpdateSerializer(
            instance=profile, data=data, partial=True
        )
        profile_serializer.is_valid(raise_exception=True)
        profile_serializer.save()


class UserSearchListSerializer(ExtendedModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'full_name',
        )
