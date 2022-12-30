from django.contrib.auth.models import AbstractUser
from django.db import models


# django.db.utils.IntegrityError: FOREIGN KEY constraint failed
# https://vk.com/@-145981744-sbros-migracii-django-udalenie-suschestvuuschei-bazy-dannyh
# TODO: Нужно перенести CATEGORIES в другое место.
#  https://clck.ru/339xxr

class Interests(models.Model):
    interests_text = models.CharField(max_length=1024)


class City(models.Model):
    city_name = models.CharField(max_length=128)


class Gender(models.Model):
    sex = models.CharField(max_length=1)


class UserQue(AbstractUser):
    """
    Custom user model
    """

    # GENDER = (
    #     ("male", "male"),
    #     ("female", "female")
    # )
    #
    CATEGORIES = (
        ("Cars", "Cars"),
        ("Books", "Books"),
        ("Football", "Football"),
    )
    middle_name = models.CharField(max_length=32, null=True)
    telegram_username = models.CharField(max_length=32)
    first_login = models.DateTimeField(null=True)
    phone = models.CharField(max_length=14)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, blank=True, default=1)
    birthday = models.DateTimeField(blank=True, null=True)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, default=1)
    language = models.CharField(max_length=8, null=True)
    favorite_categories = models.CharField(max_length=32, choices=CATEGORIES)
    avatar = models.ImageField(upload_to="user/avatar/", blank=True, null=True)
    interests = models.ManyToManyField(Interests, verbose_name='user interests')


class UserAssumption(models.Model):
    user = models.ForeignKey(UserQue, on_delete=models.CASCADE)
    needed_city = models.ForeignKey(City, on_delete=models.CASCADE, default=1)
    need_distance = models.FloatField()
    need_couple_sex = models.ForeignKey(Gender, on_delete=models.CASCADE, default=1)
    need_couple_age_min = models.IntegerField()
    need_couple_age_max = models.IntegerField()



