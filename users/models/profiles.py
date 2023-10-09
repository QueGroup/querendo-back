from datetime import date

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from users.models import Interest


class Profile(models.Model):
    class Meta:
        app_label = 'users'
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    user = models.OneToOneField(
        to='users.User', on_delete=models.CASCADE,
        related_name='profile', primary_key=True,
    )

    gender = models.CharField(
        verbose_name="пол пользователя", max_length=16, null=True, blank=True
    )

    date_of_birth = models.DateField(null=True, blank=True)
    occupation = models.CharField(
        verbose_name='Занятость', max_length=64, null=True, blank=True
    )
    ideal_match = models.CharField(
        max_length=20, null=True, blank=True
    )
    interests = models.ManyToManyField(
        verbose_name="Интересы", blank=True, to=Interest
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
    need_distance = models.IntegerField(verbose_name='Расстояние (км)', null=True)

    def calculate_age(self):
        today = date.today()
        birthdate = self.date_of_birth
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        return age

    def __str__(self):
        return f"{self.user} ({self.pk})"
