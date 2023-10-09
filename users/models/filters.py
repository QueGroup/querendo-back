from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Filters(models.Model):
    class Meta:
        app_label = 'users'
        verbose_name = 'Фильтр пользователя'
        verbose_name_plural = 'Фильтры пользователей'

    user = models.OneToOneField(
        to='users.User', related_name='filters', on_delete=models.CASCADE
    )
    radius = models.FloatField(
        verbose_name='Радиус (в километрах)', null=True, blank=True,
    )
    gender = models.CharField(
        verbose_name='Пол партнера', null=True, blank=True, max_length=16
    )
    min_age = models.PositiveIntegerField(
        verbose_name="Минимальный возраст", null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(90)]
    )
    max_age = models.PositiveIntegerField(
        verbose_name="Максимальный возраст", null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(90)]
    )
