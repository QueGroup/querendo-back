from datetime import date

from django.contrib.gis.measure import Distance, D
from django.core.validators import MinValueValidator, MaxValueValidator

from users.base.services import image_filename
from django.db import models

from django.contrib.gis.geos import Point


class Interest(models.Model):
    class Meta:
        verbose_name = 'Интерес'
        verbose_name_plural = 'Интересы'

    name = models.CharField(
        verbose_name='интересы', max_length=32, null=True, blank=True
    )

    def __str__(self):
        return f'{self.name}'


class Profile(models.Model):
    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    user = models.OneToOneField(
        to='users.User', on_delete=models.CASCADE,
        related_name='profile', primary_key=True,
    )
    telegram_id = models.PositiveBigIntegerField(
        verbose_name='Телеграм ID', null=True, blank=True
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
        verbose_name="Интересы", to=Interest, blank=True
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
        verbose_name='Пол партнера', null=True, blank=True,
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


class UserPhotos(models.Model):
    class Meta:
        verbose_name = 'Фотография пользователя'
        verbose_name_plural = 'Фотографии пользователей'

    user = models.OneToOneField(
        to='users.User', related_name='photos', on_delete=models.CASCADE
    )
    photo1 = models.ImageField(
        upload_to=image_filename)
    photo2 = models.ImageField(
        upload_to=image_filename, blank=True, null=True
    )
    photo3 = models.ImageField(
        upload_to=image_filename, blank=True, null=True
    )
    photo4 = models.ImageField(
        upload_to=image_filename, blank=True, null=True
    )
    photo5 = models.ImageField(
        upload_to=image_filename, blank=True, null=True
    )
    photo6 = models.ImageField(
        upload_to=image_filename, blank=True, null=True
    )

    def __str__(self):
        return f"{self.user}'s photos"
