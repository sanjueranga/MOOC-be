from rest_framework import serializers
from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            "title",
            "offered_by",
            "duration",
            "header_img",
            "description",
            "price",
            "tags",
        ]
