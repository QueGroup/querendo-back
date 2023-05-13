from users.base.services import image_filename
from django.db import models

from users.models.types import PositiveAgeIntegerField


class Profile(models.Model):
    user = models.OneToOneField(
        to='users.User', on_delete=models.CASCADE,
        related_name='profile', primary_key=True,
    )
    gender = models.CharField(
        verbose_name="user's gender", max_length=16, null=True, blank=True
    )
    age = PositiveAgeIntegerField(
        verbose_name="user's age", null=True, blank=True
    )
    telegram_id = models.PositiveBigIntegerField(
        verbose_name='Телеграм ID', null=True, blank=True
    )

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return f"{self.user} ({self.pk})"


class UserPhotos(models.Model):
    user = models.OneToOneField(to='users.User', related_name='photos', on_delete=models.CASCADE)
    photo1 = models.ImageField(upload_to=image_filename)
    photo2 = models.ImageField(upload_to=image_filename, blank=True, null=True)
    photo3 = models.ImageField(upload_to=image_filename, blank=True, null=True)
    photo4 = models.ImageField(upload_to=image_filename, blank=True, null=True)
    photo5 = models.ImageField(upload_to=image_filename, blank=True, null=True)
    photo6 = models.ImageField(upload_to=image_filename, blank=True, null=True)

    class Meta:
        verbose_name = 'Фотография пользователя'
        verbose_name_plural = 'Фотографии пользователей'

    def __str__(self):
        return f"{self.user}'s photos"
