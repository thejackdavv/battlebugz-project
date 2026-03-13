from django.db import models
from django.utils import timezone

from common.managers import SoftDeleteManager


# Create your models here.

class TimeStamp(models.Model):
    time_stamp = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])
        return (1, {self._meta.label: 1})

    def hard_delete(self, using=None, keep_parents=False):
        return super().delete(using=using, keep_parents=keep_parents)

    def restore(self):
        self.deleted_at = None
        self.save(update_fields=['deleted_at'])

    class Meta:
        abstract = True