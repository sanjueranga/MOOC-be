from django.contrib import admin
from .models import (
   Course
)


class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "offered_by", "duration", "price", "approved", "published")


admin.site.register(Course, CourseAdmin)