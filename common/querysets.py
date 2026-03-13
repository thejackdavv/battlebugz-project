from django.db import models
from django.utils import timezone


class SoftDeleteQuerySet(models.QuerySet):
    def delete(self, using=None, keep_parents=False):
        updated = super().update(deleted_at=timezone.now())
        if updated == 0:
            return 0, {}
        return updated, {self.model._meta.label: updated}
    def hard_delete(self):
        return super().delete()
    def existing(self):
        return self.filter(deleted_at__isnull=True)
    def deleted(self):
        return self.filter(deleted_at__isnull=False)

