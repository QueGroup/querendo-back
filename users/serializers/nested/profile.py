from common.serializers.mixins import ExtendedModelSerializer
from users.models.profiles import Profile, Interest
from rest_framework import serializers

class InterestSerializer(ExtendedModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = Interest
        fields = (
            "__all__"
        )


class ProfileShortSerializer(ExtendedModelSerializer):
    interests = InterestSerializer(many=True)

    class Meta:
        model = Profile
        fields = (
            'gender',
            'age',
            'date_of_birth',
            'occupation',
            'description',
            'language',
            'country',
            'city',
            'longitude',
            'latitude',
            'interests',
        )


class ProfileUpdateSerializer(ExtendedModelSerializer):
    interests = InterestSerializer(many=True)

    class Meta:
        model = Profile
        fields = (
            'gender',
            'age',
            'date_of_birth',
            'occupation',
            'description',
            'language',
            'country',
            'city',
            'longitude',
            'latitude',
            'interests',
        )

    def create_or_update_interests(self, interests):
        interests_ids = []
        for interest in interests:
            package_instance, created = Interest.objects.update_or_create(pk=interest.get('id'), defaults=interest)
            interests_ids.append(package_instance.pk)
        return interests_ids

    def update(self, instance, validated_data):
        interests = validated_data.pop('interests', [])
        instance.interests.set(self.create_or_update_interests(interests))
        fields = (
            "__all__"
        )
        for field in fields:
            try:
                setattr(instance, field, validated_data[field])
            except KeyError:  # validated_data may not contain all fields during HTTP PATCH
                pass
        instance.save()
        return instance
