from django.db import models

from users.base.services import image_filename


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
