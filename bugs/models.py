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
        max_length=100,
        choices=BugTypeChoices,
    )

    max_health_points = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),
        ],
        verbose_name='Health Points',
    )

    armor = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),
        ],
    )

    strength = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),
        ],
    )

    mobility = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),
        ],
    )

    healing_factor = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),
        ],
    )

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

    description = models.TextField(
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.is_active:
            Bug.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('name',)