from django.db import models

from src.profiles.models import QueUser


class Likes(models.Model):
    owner = models.ForeignKey(QueUser, on_delete=models.CASCADE, related_name="subject_id")
    liked = models.ForeignKey(QueUser, on_delete=models.CASCADE, related_name="object_id")

    def __str__(self):
        return f"{self.pk}"
