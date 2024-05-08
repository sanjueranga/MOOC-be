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


class AuthenticationType(models.Model):
    label = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.label


class UserProfile(models.Model):
    user_type_choices = (
        ("admin", "admin"),
        ("student", "student"),
        ("teacher", "teacher"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.CharField(max_length=100, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, blank=False)
    description = models.TextField(max_length=1000, blank=True, null=True)
    birth_date = models.DateField()
    user_type = models.CharField(
        max_length=100, choices=user_type_choices, editable=False, default="student"
    )
    interests = models.ManyToManyField(Interest, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Degree(models.Model):
    label = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.label


class Institution(models.Model):
    label = models.CharField(max_length=100, unique=True)
    profile_picture = models.CharField(max_length=100, blank=True, null=True)
    country = models.ForeignKey(
        Country, on_delete=models.PROTECT, blank=True, null=True
    )

    def __str__(self):
        return self.label


class Education(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, on_delete=models.PROTECT)
    degree = models.ForeignKey(Degree, on_delete=models.PROTECT)
    field_of_study = models.CharField(max_length=100)
    start_date = models.CharField(max_length=7)
    end_date = models.CharField(max_length=7)

    def __str__(self):
        return f"{self.user_profile.user.username}'s Education"


class WorkExperience(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    company = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    start_date = models.CharField(max_length=7)
    end_date = models.CharField(max_length=7)
    profile_picture = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user_profile.user.username}'s Work Experience"
