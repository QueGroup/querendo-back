from django.contrib.auth.password_validation import (
    validate_password,
)
from rest_framework import (
    serializers,
)
from rest_framework.exceptions import (
    ParseError,
)
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
)
from rest_framework_simplejwt.tokens import (
    RefreshToken,
)

from common.serializers.mixins import (
    ExtendedModelSerializer,
)
from users.models.users import (
    User,
)


class RegistrationSerializer(ExtendedModelSerializer):
    email = serializers.EmailField
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'password',
        )

    @staticmethod
    def validate_email(value: str):
        email = value.lower()
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
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


class TelegramRegistration(ExtendedModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "telegram_id",
            "username",
            "password",
        )

    @staticmethod
    def validate_username(value: str):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Это имя пользователя уже занято.")
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


class TelegramTokenCreateSerializer(TokenObtainPairSerializer):
    username = serializers.CharField()
    telegram_id = serializers.IntegerField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs: dict[str, int, str]):
        username = attrs.get('username')
        telegram_id = attrs.get('telegram_id')
        password = attrs.get('password')

        try:
            user = User.objects.get(username=username, telegram_id=telegram_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid username or telegram_id.")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid password.")

        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
