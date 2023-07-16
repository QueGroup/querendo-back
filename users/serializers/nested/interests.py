from rest_framework import serializers

from common.serializers.mixins import ExtendedModelSerializer
from users.models import Interest


class InterestSerializer(ExtendedModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Interest
        fields = (
            "id",
            "name"
        )


class InterestUpdateSerializer(ExtendedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Interest
        fields = (
            "id",
            "name"
        )
