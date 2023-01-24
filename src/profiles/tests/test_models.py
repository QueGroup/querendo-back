import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django

django.setup()
import pytest
from django.test import TestCase
from src.profiles.models import Interests, Photo, QueUser, Profile, SocialLink


class TestInterestsModel(TestCase):
    @pytest.mark.django_db
    def test_interests_creation(self):
        interest = Interests.objects.create(
            interests='test_interest'
        )
        assert interest.id is not None
        assert interest.interests == 'test_interest'

    @pytest.mark.django_db
    def test_queuser_interests_relationship(self):
        interest = Interests.objects.create(interests='test_interest')
        user = QueUser.objects.create(username='test_user')
        user.interests.add(interest)
        assert user.interests.count() == 1
        assert user.interests.first() == interest


class TestPhotoModel(TestCase):
    @pytest.mark.django_db
    def test_photo_creation(self):
        photo = Photo.objects.create(
            image='example.jpg'
        )
        assert photo.id is not None
        assert photo.image.name == 'example.jpg'

    @pytest.mark.django_db
    def test_queuser_avatar_relationship(self):
        photo = Photo.objects.create(image='example.jpg')
        user = QueUser.objects.create(username='test_user')
        user.avatar.add(photo)
        assert user.avatar.count() == 1
        assert user.avatar.first() == photo


class TestQueUserModel(TestCase):
    @pytest.mark.django_db
    def test_queuser_creation(self):
        user = QueUser.objects.create(
            username='test_user',
            phone='1234567890',
            gender='M',
            birthday='2000-01-01',
            education='test_education',
            show_me='F',
        )
        assert user.id is not None
        assert user.username == 'test_user'
        assert user.phone == '1234567890'
        assert user.gender == 'M'
        assert user.birthday == '2000-01-01'
        assert user.education == 'test_education'
        assert user.show_me == 'F'


class TestProfileModel(TestCase):
    @pytest.mark.django_db
    def test_profile_creation(self):
        user = QueUser.objects.create(username='test_user')
        profile = Profile.objects.create(
            user=user,
            bio='test_bio',
        )
        assert profile.id is not None
        assert profile.user == user
        assert profile.bio == 'test_bio'


class TestSocialLinkModel(TestCase):
    @pytest.mark.django_db
    def test_sociallink_creation(self):
        user = QueUser.objects.create(username='test_user')
        social_link = SocialLink.objects.create(
            user=user,
            link='https://example.com',
        )
        assert social_link.id is not None
        assert social_link.user == user
        assert social_link.link == 'https://example.com'
