from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import CourseSerializer
from .models import Course


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
