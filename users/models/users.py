from datetime import date

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from common.models.mixins import TimeBasedMixin
from users.managers import CustomUserManager


class CustomUser(AbstractBaseUser):
    pass


# AbstractUser
class User(TimeBasedMixin):
    id = models.AutoField(primary_key=True)
    telegram_id = models.PositiveBigIntegerField(
        unique=True, verbose_name="ID пользователя Телеграм"
    )
    username = models.CharField(
        verbose_name="Никнейм", max_length=256, unique=True
    )
    first_name = models.CharField(
        verbose_name="first name", max_length=150, blank=True
    )
    last_name = models.CharField(
        verbose_name="last name", max_length=150, blank=True
    )
    phone_number = PhoneNumberField(
        verbose_name="Телефон", unique=True, null=True, blank=True
    )
    is_verified = models.BooleanField(
        verbose_name="Подтвержденный аккаунт", default=False
    )
    gender = models.CharField(
        verbose_name="пол пользователя", max_length=16, null=True, blank=True
    )
    age = models.PositiveIntegerField(
        verbose_name="Возраст пользователя", null=True, blank=True,
        validators=[MinValueValidator(10), MaxValueValidator(90)]
    )
    date_of_birth = models.DateField(
        verbose_name="День рождения", null=True, blank=True
    )
    occupation = models.CharField(
        verbose_name="Занятость", max_length=64, null=True, blank=True
    )
    ideal_match = models.CharField(
        verbose_name="Идеальная пара", max_length=20, null=True, blank=True
    )
    interests = models.ManyToManyField(
        verbose_name="Интересы", blank=True, to="Interest"
    )
    description = models.CharField(
        verbose_name="Описание профиля", max_length=512, null=True, blank=True
    )
    language = models.CharField(
        verbose_name="Язык", max_length=16, null=True, blank=True
    )
    country = models.CharField(
        verbose_name="Страна", max_length=32, null=True, blank=True,
    )
    city = models.CharField(
        verbose_name="Город", max_length=32, blank=True, null=True,
    )
    longitude = models.FloatField(
        verbose_name="Долгота", null=True, blank=True
    )
    latitude = models.FloatField(
        verbose_name="Широта", null=True, blank=True
    )
    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["telegram_id"]

    def __str__(self):
        return f"{self.username} ({self.pk})"

    def calculate_age(self):
        today = date.today()

        try:
            birthday = self.date_of_birth.replace(year=today.year)
        except ValueError:
            birthday = self.date_of_birth.replace(year=today.year + 1)

        if birthday > today:
            age = today.year - self.date_of_birth.year - 1
        else:
            age = today.year - self.date_of_birth.year

        return age

    def get_distance_to(self, profile):
        user_location = Point(self.longitude, self.latitude, srid=4326)
        profile_location = Point(profile.longitude, profile.latitude, srid=4326)
        distance = user_location.distance(profile_location) * Distance(km=1)
        return distance.km

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
