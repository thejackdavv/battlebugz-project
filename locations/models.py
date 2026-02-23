from django.db import models

from common.models import TimeStamp


# Create your models here.

class Location(models.Model):
    class LocationTypeChoices(models.TextChoices):
        FIRE = 'FIRE', 'Fire'
        WATER = 'WATER', 'Water'
        EARTH = 'EARTH', 'Earth'
        GRASS = 'GRASS', 'Grass'

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    type = models.CharField(
        max_length=10,
        choices=LocationTypeChoices,
        db_index=True,
    )

    image_url = models.URLField(
        verbose_name='Location Image'
    )

    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Food(models.Model):
    class StatChoices(models.TextChoices):
        MAX_HP = 'MAX_HP', 'Health Points'
        ARMOR = 'ARMOR', 'Armor'
        STRENGTH = 'STRENGTH', 'Strength'
        MOBILITY = 'MOBILITY', 'Mobility'
        HEALING_FACTOR = 'HEALING_FACTOR', 'Healing Factor'

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    stat = models.CharField(
        max_length=20,
        choices=StatChoices,
    )

    increase_amount = models.PositiveIntegerField(default=1)

    location = models.ManyToManyField(
        to='Location',
        blank=True,
        related_name='foods'
    )

    def __str__(self):
        return self.name

class FoodEvent(TimeStamp):

    bug = models.ForeignKey(
        to='bugs.Bug',
        null=True,
        on_delete=models.SET_NULL,
        related_name='food_events',
    )

    location = models.ForeignKey(
        to='Location',
        null=True,
        on_delete=models.SET_NULL,
        related_name='food_events',
    )

    food = models.ForeignKey(
        to='Food',
        null=True,
        on_delete=models.SET_NULL,
        related_name='food_events',
    )
