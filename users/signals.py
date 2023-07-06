from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models.profiles import Profile
from users.models.users import User


@receiver(post_save, sender=User)
def post_save_user(sender, instance, created, **kwargs):
    if not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)
