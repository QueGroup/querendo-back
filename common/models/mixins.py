from django.db import models
from django.utils import timezone


class TimeBasedMixin(models.Model):
    created_at = models.DateTimeField(
        verbose_name='Created at', auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name='Updated at', auto_now=True
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk and not self.created_at:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(TimeBasedMixin, self).save(*args, **kwargs)
