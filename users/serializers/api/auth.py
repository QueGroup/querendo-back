from rest_framework import (
    serializers,
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


# TODO: Поле password все равно осталось обязательным
class TelegramTokenCreateSerializer(TokenObtainPairSerializer):
    username = serializers.CharField()
    telegram_id = serializers.IntegerField()

    def validate(self, attrs: dict[str, int, str]):
        username = attrs.get('username')
        telegram_id = attrs.get('telegram_id')

        try:
            user = User.objects.get(username=username, telegram_id=telegram_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid username or telegram_id.")

        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
