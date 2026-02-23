from django.db import models

from common.models import TimeStamp


# Create your models here.

class Battle(TimeStamp):
    attacker = models.ForeignKey(
        to='bugs.Bug',
        on_delete=models.PROTECT,
        related_name='battles_as_attacker',
    )

    defender = models.ForeignKey(
        to='bugs.Bug',
        on_delete=models.PROTECT,
        related_name='battles_as_defender',
    )

    location = models.ForeignKey(
        to='locations.Location',
        on_delete=models.PROTECT,
        related_name='battles',
    )

    winner = models.ForeignKey(
        to='bugs.Bug',
        on_delete=models.PROTECT,
        related_name='won_battles',
    )

    rounds = models.PositiveIntegerField(default=0)

    log = models.JSONField(
        default=list,
        blank=True,
    )