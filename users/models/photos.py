from django.db import models

from users.base.services import image_filename, IncrementalFilename, validate_size_image


class Photo(models.Model):
    class Meta:
        app_label = 'users'
        verbose_name = 'Фотография пользователя'
        verbose_name_plural = 'Фотографии пользователей'

    user = models.OneToOneField(
        to='users.User', related_name='photos', on_delete=models.CASCADE
    )
    photo1 = models.ImageField(
        upload_to=image_filename
    )
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
    file_id1 = models.CharField(
        max_length=255, blank=True, null=True
    )
    file_id2 = models.CharField(
        max_length=255, blank=True, null=True
    )
    file_id3 = models.CharField(
        max_length=255, blank=True, null=True
    )
    file_id4 = models.CharField(
        max_length=255, blank=True, null=True
    )
    file_id5 = models.CharField(
        max_length=255, blank=True, null=True
    )

    def __str__(self):
        return f"{self.user}'s photos"


class BrandBook(models.Model):
    class Meta:
        app_label = 'users'
        verbose_name = "Брендбук"
        verbose_name_plural = "Брендбук"

    name_of_page = models.CharField(
        verbose_name="Название страницы", max_length=64, null=True, blank=True
    )
    photo = models.ImageField(
        upload_to=IncrementalFilename(), verbose_name="Фотография"
    )
