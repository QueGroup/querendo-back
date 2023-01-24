from datetime import date

from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models

from src.base.services import get_path_upload_avatar, validate_size_image


class Interests(models.Model):
    """
    A model for selecting interests
    https://pypi.org/project/django-multiselectfield/
    https://stackoverflow.com/questions/27440861/django-model-multiplechoice
    """
    interests = models.CharField(max_length=64, null=True)


class Photo(models.Model):
    image = models.ImageField(upload_to=get_path_upload_avatar, blank=True, null=True,
                              validators=[
                                  FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg']),
                                  validate_size_image])


class QueUser(AbstractUser):
    """
    User Model
    """
    GENDERS = [
        ("M", "Male"),
        ("F", "Female"),
    ]
    USERS_LIST = [
        ("M", "Male"),
        ("F", "Female"),
        ("A", "All")
    ]
    phone = models.CharField(max_length=16, null=True)
    gender = models.CharField(max_length=1, choices=GENDERS, null=True)
    education = models.CharField(max_length=32, null=True)
    show_me = models.CharField(max_length=1, choices=GENDERS, null=True)
    interests = models.ManyToManyField(Interests, limit_choices_to={'id__lte': 6}, blank=True)
    avatar = models.ManyToManyField(Photo, limit_choices_to={'pk__lte': 6}, blank=True)
    birthday = models.DateField(null=True)

    @property
    def age(self):
        return int((date.today() - self.birth_date).days / 365.25)


class Profile(models.Model):
    """
    User profile model
    """
    user = models.ForeignKey(QueUser, on_delete=models.CASCADE)
    bio = models.TextField(max_length=512, null=True)


class SocialLink(models.Model):
    """
    The model of links to social networks
    """
    user = models.ForeignKey(QueUser, on_delete=models.CASCADE, related_name="social_links")
    link = models.URLField(max_length=128, null=True)

    def __str__(self):
        return "{user}".format(user=self.user)
