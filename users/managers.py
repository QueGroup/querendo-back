from typing import Optional, Any

from django.contrib.auth.base_user import BaseUserManager
from rest_framework.exceptions import ParseError


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(
            self,
            phone_number: Optional[str] = None,
            email: Optional[str] = None,
            password: Optional[str] = None,
            username: Optional[str] = None,
            **extra_fields: Any,
    ) -> Any:
        if not (email or phone_number or username):
            raise ParseError("Укажите email или телефон")

        if email:
            email = self.normalize_email(email)

        if not username:
            if email:
                username = email
            else:
                username = phone_number
        user = self.model(username=username, **extra_fields)

        if email:
            user.email = email
        if phone_number:
            user.phone_number = phone_number

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
            self,
            phone_number: Optional[str] = None,
            email: Optional[str] = None,
            password: Optional[str] = None,
            username: Optional[str] = None,
            **extra_fields: Any
    ):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', True)

        return self._create_user(
            phone_number, email, password, username, **extra_fields
        )

    def create_superuser(
            self,
            phone_number: Optional[str] = None,
            email: Optional[str] = None,
            password: Optional[str] = None,
            username: Optional[str] = None,
            **extra_fields: Any
    ):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        return self._create_user(
            phone_number, email, password, username, **extra_fields
        )