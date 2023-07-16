from datetime import date

from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Profile(models.Model):
    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    user = models.OneToOneField(
        to='users.User', on_delete=models.CASCADE,
        related_name='profile', primary_key=True,
    )

    gender = models.CharField(
        verbose_name="пол пользователя", max_length=16, null=True, blank=True
    )
    age = models.PositiveIntegerField(
        verbose_name="Возраст пользователя", null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(90)]
    )

    date_of_birth = models.DateField(null=True, blank=True)
    occupation = models.CharField(
        verbose_name='Занятость', max_length=64, null=True, blank=True
    )
    ideal_match = models.CharField(
        max_length=20, null=True, blank=True
    )
    interests = models.ManyToManyField(
        verbose_name="Интересы", blank=True, to="Interest"
    )
    description = models.CharField(
        verbose_name='Описание профиля', max_length=512, null=True, blank=True
    )
    language = models.CharField(
        verbose_name='Язык', max_length=16, null=True, blank=True
    )
    country = models.CharField(
        verbose_name='Страна', max_length=32, null=True, blank=True,
    )
    city = models.CharField(
        verbose_name='Город', max_length=32, blank=True, null=True,
    )
    longitude = models.FloatField(
        verbose_name="Долгота", null=True, blank=True

    )
    latitude = models.FloatField(
        verbose_name="Широта", null=True, blank=True
    )

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

    def __str__(self):
        return f"{self.user} ({self.pk})"
