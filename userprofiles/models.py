from django.db import models
from django.contrib.auth.models import User


class Country(models.Model):
    label = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.label
