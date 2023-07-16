from django.db.models.signals import (
    post_save
)
from django.dispatch import (
    receiver
)

from users.models import (
    Filters,
    UserPhotos,
    Profile,
    User,
)


@receiver(post_save, sender=User)
def post_save_user(
        sender: object,
        instance: User,
        created: bool,
        **kwargs: dict
) -> None:
    if not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)
    if not hasattr(instance, 'filters'):
        Filters.objects.create(user=instance)
    if not hasattr(instance, 'photos'):
        UserPhotos.objects.create(user=instance)
