import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django

django.setup()
from rest_framework.test import APITestCase


class UserAPITestCase(APITestCase):
    def test_get(self):
        pass
