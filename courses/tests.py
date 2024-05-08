from contextlib import AbstractContextManager
from typing import Any
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from .models import Course
from userprofiles.models import UserProfile, Country, Institution
from django.urls import reverse


class CreateCourseTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {
            "username": "testuser@abc.com",
            "first_name": "test",
            "last_name": "user",
            "password": "testpassword",
        }
        cls.user = User.objects.create_user(**cls.user_data)
        cls.country = Country.objects.get(label="India")
        cls.user_profile_data = {
            "user": cls.user,
            "user_type": "teacher",
            "birth_date": "1990-01-01",
            "country": cls.country,
        }
        cls.user_profile = UserProfile.objects.create(**cls.user_profile_data)
        cls.token = cls.get_token(cls.user)

    @classmethod
    def get_token(cls, user):
        return str(AccessToken.for_user(user))

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.url = reverse("course-list")

    def test_create_course_with_institute(self):
        data = {
            "title": "Test Course",
            "offered_by": "1",
            "duration": "3 months",
            "header_img": "https://test.com/test.jpg",
            "description": "This is a test course",
            "price": 1000,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        institute = Institution.objects.get(id="1")
        expected_data = {
            "status": "success",
            "message": "Course created successfully",
            "data": {
                "title": "Test Course",
                "offered_by": institute.label,
                "duration": "3 months",
                "header_img": "https://test.com/test.jpg",
                "description": "This is a test course",
                "price": "1000.00",
            },
        }
        self.assertEqual(response.data, expected_data)

    def test_create_course_with_new_institute(self):
        data = {
            "title": "Test Course",
            "institution": "Test Institute",
            "duration": "3 months",
            "header_img": "https://test.com/test.jpg",
            "description": "This is a test course",
            "price": 1000,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 1)

        expected_data = {
            "status": "success",
            "message": "Course created successfully",
            "data": {
                "title": "Test Course",
                "offered_by": "Test Institute",
                "duration": "3 months",
                "header_img": "https://test.com/test.jpg",
                "description": "This is a test course",
                "price": "1000.00",
            },
        }
        self.assertEqual(response.data, expected_data)
