from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from cities_light.models import City


class TimeBasedModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Gender(models.Model):
    GENDERS = [
        ("M", "Male"),
        ("F", "Female"),
    ]
    name = models.CharField(max_length=1, choices=GENDERS, default="M")

    def __str__(self):
        return self.name


class InterestedInGender(models.Model):
    gender_id = models.ForeignKey(Gender, on_delete=models.CASCADE)

    def __str__(self):
        return self.gender_id.name


class RelationshipType(models.Model):
    RELATIONSHIP_GOALS = [
        ('S', 'Short-term'),
        ('L', 'Long-term'),
        ('M', 'Marriage'),
        ('F', 'Friendship'),
        ('NF', 'Networking/Friendship'),
        ('N/A', 'Not Available')
    ]
    relation_goals = models.CharField(max_length=3, null=True, choices=RELATIONSHIP_GOALS, default="S")

    def __str__(self):
        return self.relation_goals


class Interests(models.Model):
    """
    A model for selecting interests
    https://pypi.org/project/django-multiselectfield/
    https://stackoverflow.com/questions/27440861/django-model-multiplechoice
    """
    interests = models.CharField(max_length=64, null=True)


class PersonalityType(models.Model):
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
    personality_type = models.CharField(max_length=4, null=True, choices=PERSONALITY_TYPE, default="ESTJ")

    def __str__(self):
        return self.personality_type


class Education(models.Model):
    EDUCATION_CATEGORIES = [
        ('HS', 'High School'),
        ('AA', r'Associate\'s Degree'),
        ('BA', r'Bachelor\'s Degree'),
        ('MA', r'Master\'s Degree'),
        ('PHD', 'Doctorate'),
        ('P', 'Professional Degree'),
        ('N/A', 'Not Available')
    ]
    name = models.CharField(max_length=32, null=True, choices=EDUCATION_CATEGORIES, default="HS")

    def __str__(self):
        return self.name


class ZodiacSign(models.Model):
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
    zodiac_sign = models.CharField(max_length=16, null=True, choices=ZODIAC_SIGN, default="leo")

    def __str__(self):
        return self.zodiac_sign


class QueUser(AbstractUser, TimeBasedModel):
    """
    User Model
    """
    telegram_id = models.IntegerField(unique=True, default=1, verbose_name="ID пользователя Телеграм")
    gender_id = models.ForeignKey(Gender, on_delete=models.CASCADE, null=True)
    interests_id = models.ForeignKey(Interests, on_delete=models.CASCADE, null=True)
    interests_in_gender_id = models.ForeignKey(InterestedInGender, on_delete=models.CASCADE, null=True)
    education_id = models.ForeignKey(Education, on_delete=models.CASCADE, null=True)
    zodiac_sign_id = models.ForeignKey(ZodiacSign, on_delete=models.CASCADE, null=True, blank=True)
    personality_type_id = models.ForeignKey(PersonalityType, on_delete=models.CASCADE, null=True, blank=True)

    phone = models.CharField(max_length=16, null=True)
    bio = models.CharField(max_length=512, null=True)
    smart_photos = models.BooleanField(default=True,
                                       verbose_name="Функция, которая выбирает лучшую фотографию из профиля")
    birthday = models.DateField(null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)


class InterestedInRelation(models.Model):
    user_account_id = models.ForeignKey(QueUser, on_delete=models.CASCADE)
    relationship_type_id = models.ForeignKey(RelationshipType, on_delete=models.CASCADE)


class UserPhoto(models.Model):
    user_account_id = models.ForeignKey(QueUser, on_delete=models.CASCADE)
    photo = models.ImageField(blank=True, null=True)


class SocialLink(models.Model):
    """
    The model of links to social networks
    """
    user_account_id = models.ForeignKey(QueUser, on_delete=models.CASCADE, related_name="social_links")
    spotify = models.CharField(max_length=100, blank=True,
                               validators=[RegexValidator(
                                   regex='^https?://open.spotify.com/[a-zA-Z0-9]+$',
                                   message='Please enter a valid Spotify URL')])
    instagram = models.CharField(max_length=100, blank=True,
                                 validators=[RegexValidator(
                                     regex='^https?://(www\.)?instagram\.com/[a-zA-Z0-9._-]+$',
                                     message='Please enter a valid Instagram URL')])

    def __str__(self):
        return "{user}".format(user=self.user_account_id.username)


class UserPreference(models.Model):
    user_account_id = models.OneToOneField(QueUser, related_name='user_preference', on_delete=models.CASCADE,
                                           db_index=True)

    age_pref_min = models.IntegerField(blank=True,
                                       choices=[(x, str(x)) for x in range(18, 90)],
                                       default=18)
    age_pref_max = models.IntegerField(blank=True,
                                       choices=[(x, str(x)) for x in range(18, 90)], null=True)
    distance_pref_min = models.IntegerField(blank=True,
                                            choices=[(x, str(x)) for x in range(1, 200)],
                                            default=1)
    distance_pref_max = models.IntegerField(blank=True,
                                            choices=[(x, str(x)) for x in range(1, 200)], null=True)

    def __str__(self):
        return 'Preference of %s' % self.user_account_id
