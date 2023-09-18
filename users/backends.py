from typing import (
    Optional,
)

from django.db.models import (
    Q,
)
from rest_framework.request import Request

from users.models.users import (
    User,
)


class AuthBacked(object):
    # supports_object_permissions: bool = True
    # supports_anonymous_user: bool = True
    # supports_inactive_user: bool = True

    @staticmethod
    def get_user(user_id) -> Optional[User]:
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    @staticmethod
    def authenticate(request: Request, username: str) -> Optional[User]:
        try:
            user = User.objects.get(
                Q(username=username) |
                Q(phone_number=username)
            )
        except User.DoesNotExist:
            return None

        return user
