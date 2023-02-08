from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import QueUser, UserPhoto


class UserQueSerializer(serializers.ModelSerializer):
    """
    Output info about our user
    """
    avatar = serializers.ImageField(write_only=True)

    class Meta:
        model = QueUser
        exclude = (
            "password",
            "last_login",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
            "phone",
        )


class UserQuePublicSerializer(serializers.ModelSerializer):
    """
    Output public info about our user
    """
    avatar = serializers.ImageField(write_only=True)

    class Meta:
        model = QueUser
        exclude = (
            "email",
            "phone",
            "password",
            "last_login",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
        )


class TelegramUsersList(serializers.ModelSerializer):
    class Meta:
        model = QueUser
        fields = ['telegram_id', 'username', 'password', 'phone', 'birthday', 'gender', 'email']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = QueUser.objects.create(
            username=validated_data['username'],
            password=make_password(validated_data['password']),
            telegram_id=validated_data['telegram_id'],
            gender=validated_data['gender'],
            email=validated_data['email'],
            birthday=validated_data['birthday'],
            phone=validated_data['phone']
        )
        return user


# username, password, tg_id_ sms by phone number, gender, age(like a datetime), update age every year, city,
#посмотреть django cities light и разобраться с подгрузкой городов
#создать два поля с широтой и долготой
#глянуть sms шлюзы
#авторизация по почте
#глянуть асинхронную работу в django

class ImageForm(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = UserPhoto
        fields = ('image',)
