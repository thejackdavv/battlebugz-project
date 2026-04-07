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
        max_length=500,
    )

    description = models.TextField()

    owner = models.ForeignKey(
        to='accounts.Profile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bugs',
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new and self.natural_habitat:
            self.natural_habitat.inhabitants.add(self)

    @property
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
