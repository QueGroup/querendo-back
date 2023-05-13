from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class PositiveAgeIntegerField(models.PositiveIntegerField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('validators', []).extend([
            MaxValueValidator(160),
            MinValueValidator(0),
        ])
        super().__init__(*args, **kwargs)
