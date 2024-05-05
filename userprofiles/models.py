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

class UserType(models.Model):
    label = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.label
    
class AuthenticationType(models.Model):
    label = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.label
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.CharField(max_length=100, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, blank=False)
    description = models.TextField(max_length=1000)
    birth_date = models.DateField()
    user_type = models.ForeignKey(UserType, on_delete=models.PROTECT)
    authentication_type = models.ForeignKey(AuthenticationType, on_delete=models.PROTECT)
    interests = models.ManyToManyField(Interest)


    def __str__(self):
        return f"{self.user.username}'s Profile"
    

class Degree(models.Model):
    label = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.label
    
class Institution(models.Model):
    label = models.CharField(max_length=100, unique=True)
    profile_picture = models.CharField(max_length=100, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, blank=True,null=True)

    def __str__(self):
        return self.label
    
class Education(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, on_delete=models.PROTECT)
    degree = models.ForeignKey(Degree, on_delete=models.PROTECT)
    field_of_study = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(max_length=1000)

    def __str__(self):
        return f"{self.user_profile.user.username}'s Education"
    

class WorkExperience(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    company = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    profile_picture = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user_profile.user.username}'s Work Experience"