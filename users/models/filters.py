from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance, D
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from users.models.profiles import Profile


class Filters(models.Model):
    class Meta:
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

    def find_profiles(self, latitude, longitude):
        user_location = Point(longitude, latitude, srid=4326)
        profiles = Profile.objects.filter(
            gender=self.gender,
            age__range=(self.min_age, self.max_age),
            location__distance_lte=(user_location, D(km=self.radius))
        ).annotate(distance=Distance('location')).order_by('distance')
        return profiles
