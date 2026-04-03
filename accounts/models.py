from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.

UserModel = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(
        to=UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    bio = models.TextField(
        null=True,
        blank=True,
    )

    active_bug = models.ForeignKey(
        to='bugs.Bug',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.user.username
