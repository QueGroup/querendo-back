from common.serializers.mixins import ExtendedModelSerializer
from users.models.profiles import Profile, Interest


class InterestSerializer(ExtendedModelSerializer):
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
