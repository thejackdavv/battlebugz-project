from django.db import models

from common.querysets import SoftDeleteQuerySet


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).existing()