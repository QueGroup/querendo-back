from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import QueUser, Education, ZodiacSign, InterestedInRelation, SocialLink, UserPreference, UserPhotos


# TODO: https://hakibenita.com/django-rest-framework-slow


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        exclude = ('id', 'user_account_id')


class ZodiacSignSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZodiacSign
        exclude = ('id', 'user_account_id')


class InterestedInRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterestedInRelation
        exclude = ('id', 'user_account_id')


class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        exclude = ('id', 'user_account_id')


class UserPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreference
        exclude = ('id', 'user_account_id')


class UserPhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPhotos
        fields = '__all__'


class UserQuePublicSerializer(serializers.ModelSerializer):
    """
    Output a subset of info about our user for public use
    """

    education = EducationSerializer()
    zodiac_sign = ZodiacSignSerializer()
    interested_in_relation = InterestedInRelationSerializer(many=True)
    social_link = SocialLinkSerializer(many=True)
    user_preference = UserPreferenceSerializer()

    photos = UserPhotosSerializer(many=True)

    class Meta:
        model = QueUser
        exclude = (
            'password',
            'last_login',
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
            'phone',
            'updated_at',
            'email',
        )

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     return dict(data)


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = QueUser
        fields = ['id', 'username', 'email', 'telegram_id', 'is_registered']

    def validate_custom_id(self, value):
        if value and not value.isalnum():
            raise serializers.ValidationError('Custom ID should be alphanumeric')
        return value

    def validate(self, data):
        # Проверяем, что поле "username" не совпадает с полем "custom_id"
        if 'username' in data and 'custom_id' in data and data['username'] == data['custom_id']:
            raise serializers.ValidationError('Username and Custom ID cannot be the same')

        return data


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = QueUser
        fields = ['id', 'username', 'password', 'first_name', 'city', 'birthday', 'gender',
                  'interested_in_gender', 'phone', 'email']
        ref_name = 'ProfileUser'

    def create(self, validated_data: dict):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)


class TelegramUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = QueUser
        fields = [
            'id', 'username', 'password', 'first_name', 'city', 'birthday', 'gender', 'phone', 'telegram_id',
            'interested_in_gender'
        ]

    def create(self, validated_data: dict):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)


class VerifyAccountSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

    class Meta:
        model = QueUser
        fields = ('email', 'otp')


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(write_only=True, min_length=8, max_length=128)


class ConfirmOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
