from django.db import models
from django.contrib.auth.models import User


class Country(models.Model):
    label = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.label

class Interest(models.Model):
    label = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.label


class UserInterest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    interest = models.ForeignKey(Interest, on_delete=models.PROTECT)

    class Meta:
        unique_together = (
            "user",
            "interest",
        )