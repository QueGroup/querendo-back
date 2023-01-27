from datetime import date

from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator, RegexValidator
from django.db import models
from cities_light.models import City

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
    username = models.CharField(max_length=16, unique=True)
    phone = models.CharField(max_length=16, null=True)
    gender = models.CharField(max_length=1, choices=GENDERS, null=True)
    educational_experience = models.CharField(max_length=32, null=True, verbose_name="Место обучения")
    show_me = models.CharField(max_length=1, choices=GENDERS, null=True)
    interests = models.ManyToManyField(Interests, limit_choices_to={'id__lte': 6}, blank=True)
    avatar = models.ManyToManyField(Photo, limit_choices_to={'pk__lte': 6}, blank=True)
    birthday = models.DateField(null=True)

    @property
    def age(self):
        return int((date.today() - self.birth_date).days / 365.25)


class SocialLink(models.Model):
    """
    The model of links to social networks
    """
    user = models.ForeignKey(QueUser, on_delete=models.CASCADE, related_name="social_links")
    spotify = models.CharField(max_length=100, blank=True,
                               validators=[RegexValidator(
                                   regex='^https?://open.spotify.com/[a-zA-Z0-9]+$',
                                   message='Please enter a valid Spotify URL')])
    instagram = models.CharField(max_length=100, blank=True,
                                 validators=[RegexValidator(
                                     regex='^https?://(www\.)?instagram\.com/[a-zA-Z0-9._-]+$',
                                     message='Please enter a valid Instagram URL')])

    def __str__(self):
        return "{user}".format(user=self.user.username)


class Profile(models.Model):
    """
    User profile model
    """
    RELATIONSHIP_GOALS = [
        ('S', 'Short-term'),
        ('L', 'Long-term'),
        ('M', 'Marriage'),
        ('F', 'Friendship'),
        ('NF', 'Networking/Friendship'),
        ('N/A', 'Not Available')
    ]
    ZODIAC_SIGN = [
        ('aquarius', 'Aquarius'),
        ('pisces', 'Pisces'),
        ('aries', 'Aries'),
        ('taurus', 'Taurus'),
        ('gemini', 'Gemini'),
        ('cancer', 'Cancer'),
        ('leo', 'Leo'),
        ('virgo', 'Virgo'),
        ('libra', 'Libra'),
        ('scorpio', 'Scorpio'),
        ('sagittarius', 'Sagittarius'),
        ('capricorn', 'Capricorn'),
    ]
    EDUCATION_CATEGORIES = [
        ('HS', 'High School'),
        ('AA', r'Associate\'s Degree'),
        ('BA', r'Bachelor\'s Degree'),
        ('MA', r'Master\'s Degree'),
        ('PHD', 'Doctorate'),
        ('P', 'Professional Degree'),
        ('N/A', 'Not Available')
    ]

    # PLANS_FAMILY = [
    #     ("A", "B")
    # ]

    PERSONALITY_TYPE = [

        ('ISTJ', 'Introverted, Sensing, Thinking, Judging'),
        ('ISFJ', 'Introverted, Sensing, Feeling, Judging'),
        ('INFJ', 'Introverted, Intuitive, Feeling, Judging'),
        ('INTJ', 'Introverted, Intuitive, Thinking, Judging'),
        ('ISTP', 'Introverted, Sensing, Thinking, Perceiving'),
        ('ISFP', 'Introverted, Sensing, Feeling, Perceiving'),
        ('INFP', 'Introverted, Intuitive, Feeling, Perceiving'),
        ('INTP', 'Introverted, Intuitive, Thinking, Perceiving'),
        ('ESTJ', 'Extraverted, Sensing, Thinking, Judging'),
        ('ESFJ', 'Extraverted, Sensing, Feeling, Judging'),
        ('ENFJ', 'Extraverted, Intuitive, Feeling, Judging'),
        ('ENTJ', 'Extraverted, Intuitive, Thinking, Judging'),
        ('ESTP', 'Extraverted, Sensing, Thinking, Perceiving'),
        ('ESFP', 'Extraverted, Sensing, Feeling, Perceiving'),
        ('ENFP', 'Extraverted, Intuitive, Feeling, Perceiving'),
        ('ENTP', 'Extraverted, Intuitive, Thinking, Perceiving')

    ]

    user = models.OneToOneField(QueUser, on_delete=models.CASCADE)
    bio = models.TextField(max_length=512, null=True)
    smart_photos = models.BooleanField(default=True,
                                       verbose_name="Функция, которая выбирает лучшую фотографию из профиля")
    relation_goals = models.CharField(max_length=3, null=True, choices=RELATIONSHIP_GOALS)
    zodiac_sign = models.CharField(max_length=16, null=True, choices=ZODIAC_SIGN)
    education = models.CharField(max_length=32, null=True, choices=EDUCATION_CATEGORIES)
    # plans_for_family = models.CharField(max_length=32, null=True, choices=PLANS_FAMILY)
    personality_type = models.CharField(max_length=4, null=True, choices=PERSONALITY_TYPE)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    company = models.CharField(max_length=64, null=True)
