from typing import (
    Optional,
    Any,
    Union,
    NoReturn,
)

from django.contrib.auth.base_user import (
    BaseUserManager,
)
from rest_framework.exceptions import (
    ParseError,
)


class CustomUserManager(BaseUserManager):
    use_in_migrations: bool = True

    def _create_user(
            self,
            phone_number: Optional[str] = None,
            username: Optional[str] = None,
            telegram_id: Optional[int] = None,
            **extra_fields: Any,
    ) -> Union[NoReturn, "User"]:
        if not (phone_number or username or telegram_id):
            raise ParseError("Укажите email или телефон или имя пользователя или Telegram ID.")

        if not username:
            username = phone_number
        user = self.model(username=username, **extra_fields)

        if phone_number:
            user.phone_number = phone_number

        if telegram_id:
            user.telegram_id = telegram_id

        user.save(using=self._db)
        return user

    def create_user(
            self,
            phone_number: Optional[str] = None,
            username: Optional[str] = None,
            telegram_id: Optional[int] = None,
            **extra_fields: Any
    ) -> "User":
        # extra_fields.setdefault('is_superuser', False)
        # extra_fields.setdefault('is_staff', False)
        # extra_fields.setdefault('is_active', True)

        return self._create_user(
            phone_number=phone_number, username=username, telegram_id=telegram_id, **extra_fields
        )

    def create_superuser(
            self,
            telegram_id: Optional[str] = None,
            username: Optional[str] = None,
            **extra_fields: Any
    ) -> "User":
        # extra_fields.setdefault('is_superuser', True)
        # extra_fields.setdefault('is_staff', True)
        # extra_fields.setdefault('is_active', True)

        return self._create_user(
            telegram_id=telegram_id, username=username, **extra_fields
        )
