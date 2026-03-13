from django.db import models

from common.querysets import SoftDeleteQuerySet


class SoftDeleteManager(models.Manager.from_queryset(SoftDeleteQuerySet)):
    def get_queryset(self):
        return super().get_queryset().existing()