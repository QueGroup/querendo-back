from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import Filters, Photo
from users.models.profiles import Profile
from users.models.users import User


@receiver(post_save, sender=User)
def post_save_user(
        sender: object,
        instance: User,
        created: bool,
        **kwargs: dict
) -> None:
    if created:
        if not hasattr(instance, 'profile'):
            Profile.objects.create(user=instance)
        if not hasattr(instance, 'filters'):
            Filters.objects.create(user=instance)
        if not hasattr(instance, 'photos'):
            Photo.objects.create(user=instance)

