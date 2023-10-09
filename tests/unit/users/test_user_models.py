import random
import string
from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase

from users.models import Filters, UserPhotos, Profile, User


class TestCaseMixin(TestCase):
    @staticmethod
    def generate_random_string(length=10):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    @staticmethod
    def generate_random_phone_number():
        country_code = '+'
        area_code = ''.join(random.choices(string.digits, k=2))
        main_number = ''.join(random.choices(string.digits, k=7))
        return f'{country_code}{area_code}{main_number}'


class UserModelTestCase(TestCaseMixin):
    def setUp(self):
        self.User = get_user_model()

    def tearDown(self):
        self.User.objects.all().delete()
        Profile.objects.all().delete()
        Filters.objects.all().delete()
        UserPhotos.objects.all().delete()

    def test_create_user_and_related_objects(self):
        username = self.generate_random_string()
        email = self.generate_random_string() + '@example.com'
        phone_number = self.generate_random_phone_number()
        telegram_id = random.randint(10 ** 5, 10 ** 9 - 1)
        password = 'testpassword'

        self.assertEqual(self.User.objects.count(), 0)
        self.assertEqual(Profile.objects.count(), 0)
        self.assertEqual(Filters.objects.count(), 0)
        self.assertEqual(UserPhotos.objects.count(), 0)

        user = self.User.objects.create_user(
            username=username,
            email=email,
            phone_number=phone_number,
            telegram_id=telegram_id,
            password=password
        )

        self.assertEqual(self.User.objects.count(), 1)
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(Filters.objects.count(), 1)
        self.assertEqual(UserPhotos.objects.count(), 1)

        self.assertTrue(hasattr(user, 'profile'))
        self.assertTrue(hasattr(user, 'filters'))
        self.assertTrue(hasattr(user, 'photos'))

        self.assertEqual(user.username, username)
        self.assertEqual(user.email, email)
        self.assertEqual(str(user.phone_number), phone_number)
        self.assertEqual(user.telegram_id, telegram_id)
        self.assertTrue(user.check_password(password))

    def test_create_superuser(self):
        superuser = self.User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword'
        )
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)


class ProfileModelTestCase(TestCaseMixin):
    def setUp(self):
        username = self.generate_random_string()
        email = self.generate_random_string() + '@example.com'
        password = 'testpassword'

        self.user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

    def test_create_profile(self):
        profile = Profile(
            user=self.user,
            gender='M',
            date_of_birth=date(1998, 1, 1),
            occupation='Software Engineer',
            ideal_match='F',
            description='A description of the user',
            language='en',
            country='USA',
            city='New York',
            longitude=40.7128,
            latitude=-74.0060,
            need_distance=10
        )
        profile.save()

        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.gender, 'M')
        self.assertEqual(str(profile.date_of_birth), '1998-01-01')
        self.assertEqual(profile.occupation, 'Software Engineer')
        self.assertEqual(profile.ideal_match, 'F')
        self.assertEqual(profile.description, 'A description of the user')
        self.assertEqual(profile.language, 'en')
        self.assertEqual(profile.country, 'USA')
        self.assertEqual(profile.city, 'New York')
        self.assertEqual(profile.longitude, 40.7128)
        self.assertEqual(profile.latitude, -74.0060)
        self.assertEqual(profile.need_distance, 10)
        self.assertEqual(profile.calculate_age(), 25)
