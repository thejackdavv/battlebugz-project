from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.

class Bug(models.Model):
    class BugTypeChoices(models.TextChoices):
        FIRE = 'Fire', 'Fire'
        WATER = 'Water', 'Water'
        EARTH = 'Earth', 'Earth'
        GRASS = 'Grass', 'Grass'


    name = models.CharField(
        max_length=100,
        unique=True,
    )

    type = models.CharField(
        max_length=100,
        choices=BugTypeChoices,
    )

    max_health_points = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
        ],
        verbose_name='Health Points',
    )

    armor = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
        ],
    )

    strength = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
        ],
    )

    mobility = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
        ],
    )

    healing_factor = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
        ],
    )

    # natural_habitat = models.ForeignKey(
    #     to="locations.Location",
    #     on_delete=models.CASCADE,
    #     related_name='bugs',
    # )

    image_url = models.URLField(
        verbose_name='Bug Image',
    )

    is_active = models.BooleanField(
        default=False,
    )