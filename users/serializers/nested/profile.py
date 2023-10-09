from common.serializers.mixins import ExtendedModelSerializer
from users.models.profiles import Interest, Profile
from users.serializers.nested.interests import InterestSerializer


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
            'need_distance',
            'ideal_match',
        )


class ProfileUpdateSerializer(ExtendedModelSerializer):
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
            'need_distance',
            'ideal_match',
        )


class ProfileInterestUpdateSerializer(ExtendedModelSerializer):
    interests = InterestSerializer(many=True)

    class Meta:
        model = Profile
        fields = (
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
