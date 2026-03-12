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
        self.save()

    def hard_delete(self):
        super().delete()

    def restore(self):
        self.deleted_at = None
        self.save()

    class Meta:
        abstract = True