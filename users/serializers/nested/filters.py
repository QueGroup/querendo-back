from rest_framework import serializers

from users.models import Filters


class UserFilterShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filters
        fields = (
            "radius",
            "gender",
            "min_age",
            "max_age",
        )
