from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import CourseSerializer
from .models import Course


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def create(self, request, *args, **kwargs):

        response = super().create(request, *args, **kwargs)
        response.data = {
            "status": "success",
            "message": "Course created successfully",
            "data": response.data,
        }
        return response
