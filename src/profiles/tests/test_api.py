import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

django.setup()

import pytest
from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.test import APIClient
from model_bakery import baker
from src.profiles.models import QueUser


@pytest.mark.django_db
class TestUserQuePublicAPI:
    def test_retrieve_public_user_account(self):
        # user = baker.make(QueUser)
        client = APIClient()
        url = reverse_lazy('profiles:account-list')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        # assert response.data == UserQuePublicSerializer(user).data

    def test_list_public_user_accounts(self):
        baker.make(QueUser, _quantity=5)
        client = APIClient()
        url = reverse_lazy('profiles:account-list')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert set(response.data[0].keys()) == {'bio',
                                                'birthday',
                                                'birthday_dayofyear_internal',
                                                'city',
                                                'created_at',
                                                'date_joined',
                                                'education',
                                                'first_name',
                                                'gender',
                                                'id',
                                                'interested_in_gender',
                                                'interested_in_relation',
                                                'is_registered',
                                                'is_verified',
                                                'language',
                                                'last_name',
                                                'otp',
                                                'photos',
                                                'reset_password_code_expired_at',
                                                'reset_password_otp',
                                                'reset_password_requested_at',
                                                'smart_photos',
                                                'social_link',
                                                'telegram_id',
                                                'user_preference',
                                                'username',
                                                'zodiac_sign'}
