from django.utils import timezone
from django.db import models


class TimeBasedMixin(models.Model):
    created_at = models.DateTimeField('Created at', null=True, blank=False)
    updated_at = models.DateTimeField('Updated at', null=True, blank=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk and not self.created_at:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(TimeBasedMixin, self).save(*args, **kwargs)
