from rest_framework import serializers
from .models import Course
from userprofiles.models import Institution


class CourseSerializer(serializers.ModelSerializer):
    institution = serializers.CharField(required=False)

    class Meta:
        model = Course
        fields = [
            "title",
            "offered_by",
            "duration",
            "header_img",
            "description",
            "price",
            "institution",
        ]

    def validate(self, attrs):
        request = self.context["request"]
        attrs["course_creator"] = request.user
        institution_label = attrs.pop("institution", None)
        self.fields.pop("institution")
        

        return super().validate(attrs)