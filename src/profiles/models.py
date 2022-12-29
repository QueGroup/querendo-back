from django.contrib.auth.models import AbstractUser
from django.db import models


# django.db.utils.IntegrityError: FOREIGN KEY constraint failed
# https://vk.com/@-145981744-sbros-migracii-django-udalenie-suschestvuuschei-bazy-dannyh
# TODO: Нужно перенести CATEGORIES в другое место.
#  https://clck.ru/339xxr
class UserQue(AbstractUser):
    """
    Custom user model
    """

    GENDER = (
        ("male", "male"),
        ("female", "female")
    )

    CATEGORIES = (
        ("Cars", "Cars"),
        ("Books", "Books"),
        ("Football", "Football"),
    )
    middle_name = models.CharField(max_length=32, null=True)
    telegram_username = models.CharField(max_length=32)
    first_login = models.DateTimeField(null=True)
    phone = models.CharField(max_length=14)
    gender = models.CharField(max_length=6, choices=GENDER)
    birthday = models.DateTimeField(blank=True, null=True)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    city = models.CharField(max_length=32)
    language = models.CharField(max_length=8, null=True)
    favorite_categories = models.CharField(max_length=32, choices=CATEGORIES)
    avatar = models.ImageField(upload_to="user/avatar/", blank=True, null=True)
