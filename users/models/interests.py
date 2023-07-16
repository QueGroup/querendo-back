from django.db import models


class Interest(models.Model):
    class Meta:
        verbose_name = 'Интерес'
        verbose_name_plural = 'Интересы'

    name = models.CharField(
        verbose_name='интересы', max_length=64, unique=False
    )

    def __str__(self):
        return f"({self.name})"
