from django.contrib import admin
from .models import Country, Interest, UserType, AuthenticationType, UserProfile, Degree, Institution, Education, WorkExperience

class CountryAdmin(admin.ModelAdmin):
    list_display = ("label",)

class InterestAdmin(admin.ModelAdmin):
    list_display = ("label",)

class UserTypeAdmin(admin.ModelAdmin):
    list_display = ("label",)

class AuthenticationTypeAdmin(admin.ModelAdmin):
    list_display = ("label",)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "country", "birth_date", "user_type", "authentication_type")

class DegreeAdmin(admin.ModelAdmin):
    list_display = ("label",)

class InstitutionAdmin(admin.ModelAdmin):
    list_display = ("label", "country")

class EducationAdmin(admin.ModelAdmin):
    list_display = ("user_profile", "institution", "degree", "field_of_study", "start_date", "end_date")

class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ("user_profile", "company", "position", "start_date", "end_date")

admin.site.register(Country, CountryAdmin)
admin.site.register(Interest, InterestAdmin)
admin.site.register(UserType, UserTypeAdmin)
admin.site.register(AuthenticationType, AuthenticationTypeAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Degree, DegreeAdmin)
admin.site.register(Institution, InstitutionAdmin)
admin.site.register(Education, EducationAdmin)
admin.site.register(WorkExperience, WorkExperienceAdmin)