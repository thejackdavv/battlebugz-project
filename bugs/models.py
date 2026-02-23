from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.

class Bug(models.Model):
    class BugTypeChoices(models.TextChoices):
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
        choices=BugTypeChoices,
        db_index=True,
    )

    max_health_points = models.PositiveIntegerField(
        verbose_name='Health Points'
    )

    armor = models.PositiveIntegerField()

    strength = models.PositiveIntegerField()

    mobility = models.PositiveIntegerField()

    healing_factor = models.PositiveIntegerField()

    natural_habitat = models.ForeignKey(
        to="locations.Location",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bugs',
    )

    image_url = models.URLField(
        verbose_name='Bug Image',
    )

    description = models.TextField()

    is_active = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.is_active:
            Bug.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)

    def total_power(self):
        return (
            self.max_health_points +
            self.armor +
            self.strength +
            self.mobility +
            self.healing_factor
        )

    class Meta:
        ordering = ('name',)