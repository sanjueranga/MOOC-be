from contextlib import AbstractContextManager
from typing import Any
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import (
    UserProfile,
    Country,
    UserType,
    WorkExperience,
    Education,
    Institution,
    Degree,
)
from rest_framework_simplejwt.tokens import AccessToken


class UserRegisterViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("user-registration")

    def setUp(self):
        self.data = {
            "username": "testuser",
            "firstname": "first",
            "lastname": "last",
            "email": "test@gmail.com",
            "password": "password",
        }

    def create_user(self, email):
        return User.objects.create_user(
            first_name="existing",
            last_name="user",
            username=email,
            email=email,
            password="password123",
        )

    def post_request(self, data):
        return self.client.post(self.url, data)

    def test_create_user_success(self):
        response = self.post_request(self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_user = User.objects.get(email=self.data["email"])
        self.assertEqual(created_user.email, self.data["email"])

    def test_create_user_wrong_email_format(self):
        self.data["email"] = "testgmail.com"
        response = self.post_request(self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], ["Enter a valid email address."])

    def test_email_uniqueness(self):
        self.create_user("existing@example.com")
        self.data["email"] = "existing@example.com"
        response = self.post_request(self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], ["Email already exists"])

    def test_email_and_password_not_provided(self):
        del self.data["email"]
        del self.data["password"]
        response = self.post_request(self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        messages = ["email field is required.", "password field is required."]

        self.assertTrue(
            any(message in response.data["message"] for message in messages)
        )


class CreateUserProfileViewSetTest(APITestCase):

    def setUp(self):
        self.url = "/api/user/info/"
        self.user_data = {
            "username": "testuser@abc.com",
            "first_name": "test",
            "last_name": "user",
            "password": "testpassword",
        }
        self.user = self.create_user(self.user_data)
        self.token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def create_user(self, user_data):
        return User.objects.create_user(**user_data)

    def get_token(self):
        return str(AccessToken.for_user(self.user))

    def post_request(self, data):
        return self.client.post(self.url, data, format="json")

    def test_create_user_profile_success(self):
        user_data = {
            "country": "Turkey",
            "user_type": "Student",
            "profile_picture": "abc.com",
            "birth_date": "2000-10-12",
        }

        response = self.post_request(user_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        updated_user_profile = UserProfile.objects.get(user=self.user)

        self.assertEqual(updated_user_profile.country.label, user_data["country"])
        self.assertEqual(
            updated_user_profile.profile_picture, user_data["profile_picture"]
        )
        self.assertEqual(updated_user_profile.user_type.label, user_data["user_type"])

        expected_data = {
            "status": "success",
            "message": "User data added successfully",
            "data": "null",
        }
        self.assertEqual(response.data, expected_data)

    def test_create_user_profile_fail_with_missing_fields(self):
        incomplete_data = {}
        response = self.post_request(incomplete_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        expected_data = {
            "status": "fail",
            "message": [
                "country field is required.",
                "user_type field is required.",
                "birth_date field is required.",
            ],
        }

        self.assertEqual(set(response.data["message"]), set(expected_data["message"]))

    def test_create_user_profile_fail_wrong_data_types(self):
        user_data_country = {
            "username": "bravo9161",
            "country": "Turkeydafd",
            "user_type": "Student",
            "profile_picture": "abc.com",
            "birth_date": "2000-10-12",
        }

        response = self.post_request(user_data_country)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        expected_data = {"status": "fail", "message": ["Invalid country name provided"]}
        self.assertEqual(response.data, expected_data)

        user_data_user_type = {
            "username": "bravo9161",
            "country": "Turkey",
            "user_type": "Studentfd",
            "profile_picture": "abc.com",
            "birth_date": "2000-10-12",
        }

        response = self.post_request(user_data_user_type)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        expected_data = {"status": "fail", "message": ["Invalid user type provided"]}
        self.assertEqual(response.data, expected_data)


class UpdateUserProfileTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("user-info")
        cls.user_data = {
            "username": "testuser@abc.com",
            "email": "testuser@abc.com",
            "first_name": "test",
            "last_name": "user",
            "password": "testpassword",
        }
        cls.country = Country.objects.get(label="Turkey")
        cls.profile_data = {
            "country": cls.country,
            "user_type": UserType.objects.get(label="Student"),
            "birth_date": "2000-10-12",
            "description": "lorem ipsum dolor sit amet",
            "profile_picture": "url",
        }
        cls.user = User.objects.create_user(**cls.user_data)
        cls.user_profile = UserProfile.objects.create(user=cls.user, **cls.profile_data)
        cls.token = str(AccessToken.for_user(cls.user))

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_update_user_profile_success_functionality(self):
        user_data = {
            "username": "new_username",
            "firstname": "John2",
            "lastname": "Doe2",
            "country": "Sri Lanka",
            "profile_picture": "abc.com",
            "birth_date": "2000-10-13",
            "description": "user bio",
        }
        response = self.client.put(self.url, user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_user_profile = UserProfile.objects.get(user=self.user)

        self.assertEqual(updated_user_profile.user.username, user_data["username"])
        self.assertEqual(updated_user_profile.user.first_name, user_data["firstname"])
        self.assertEqual(updated_user_profile.user.last_name, user_data["lastname"])
        self.assertEqual(updated_user_profile.country.label, user_data["country"])
        self.assertEqual(updated_user_profile.description, user_data["description"])
        self.assertEqual(
            updated_user_profile.profile_picture, user_data["profile_picture"]
        )

    def test_update_user_profile_success_message(self):

        user_data = {
            "username": "new_username",
            "firstname": "John2",
            "lastname": "Doe2",
            "country": "Sri Lanka",
            "profile_picture": "abc.com",
            "birth_date": "2000-10-13",
            "description": "user bio",
        }
        response = self.client.put(self.url, user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_response = {
            "status": "success",
            "message": "User data updated successfully",
            "data": None,
        }
        self.assertEqual(set(response.data), set(expected_response))

    def test_create_user_profile_fail_duplicate_username(self):
        another_user = {
            "username": "updated_username",
            "first_name": "test",
            "last_name": "user",
            "password": "testpassword",
        }

        duplicate_user = User.objects.create_user(**another_user)
        user_data = {
            "username": duplicate_user.username,
            "firstname": "John2",
            "lastname": "Doe2",
            "country": "Sri Lanka",
            "profile_picture": "abc.com",
            "birth_date": "2000-10-13",
            "description": "user bio",
        }

        response = self.client.put(self.url, user_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        expected_data = {"status": "fail", "message": ["Username already exists"]}
        self.assertEqual(response.data, expected_data)

    def test_create_user_profile_fail_wrong_data_types(self):

        user_data_country = {
            "username": "new_username",
            "firstname": "John2",
            "lastname": "Doe2",
            "country": "Sri Ladddnka",
            "profile_picture": "abc.com",
            "birth_date": "2000-10-13",
            "description": "user bio",
        }

        response = self.client.put(self.url, user_data_country, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        expected_data = {"status": "fail", "message": ["Invalid country name provided"]}
        self.assertEqual(response.data, expected_data)

    def test_user_type_is_not_updated(self):
        user_data = {
            "username": "new_username",
            "firstname": "John2",
            "lastname": "Doe2",
            "country": "Sri Lanka",
            "profile_picture": "abc.com",
            "birth_date": "2000-10-13",
            "description": "user bio",
            "user_type": "Teacher",
        }

        response = self.client.put(self.url, user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_user_profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(updated_user_profile.user_type.label, "Student")


class WorkExperienceViewSetTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("user-info")
        cls.user_data = {
            "username": "testuser@abc.com",
            "email": "testuser@abc.com",
            "first_name": "test",
            "last_name": "user",
            "password": "testpassword",
        }
        cls.country = Country.objects.get(label="Turkey")
        cls.profile_data = {
            "country": cls.country,
            "user_type": UserType.objects.get(label="Student"),
            "birth_date": "2000-10-12",
            "description": "lorem ipsum dolor sit amet",
            "profile_picture": "url",
        }
        cls.user = User.objects.create_user(**cls.user_data)
        cls.user_profile = UserProfile.objects.create(user=cls.user, **cls.profile_data)
        cls.token = str(AccessToken.for_user(cls.user))

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.url = reverse("work-experience")

    def test_add_work_experience_success(self):
        work_data = {
            "position": "Software Engineer",
            "company": "Google",
            "start_date": "2020-10",
            "end_date": "2021-10",
        }
        response = self.client.post(self.url, work_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], "success")
        self.assertEqual(
            response.data["message"], "WorkExperience data added successfully"
        )

    def test_update_work_experience_success(self):
        work_data = {
            "position": "Software Engineer",
            "company": "Google",
            "start_date": "2020-10",
            "end_date": "2021-10",
        }
        work = WorkExperience.objects.create(
            user_profile=self.user_profile, **work_data
        )
        work_id = work.id
        work_data = {
            "position": "Software Engineer",
            "company": "Google",
            "start_date": "2020-10",
            "end_date": "2021-10",
        }
        response = self.client.put(
            f"/api/user/work/{work_id}/", work_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "success")
        self.assertEqual(
            response.data["message"], "WorkExperience updated successfully"
        )

    def test_delete_work_experience_success(self):
        work_data = {
            "position": "Software Engineer",
            "company": "Google",
            "start_date": "2020-10",
            "end_date": "2021-10",
        }
        work = WorkExperience.objects.create(
            user_profile=self.user_profile, **work_data
        )
        work_id = work.id
        response = self.client.delete(f"/api/user/work/{work_id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data["status"], "success")
        self.assertEqual(
            response.data["message"], "WorkExperience deleted successfully"
        )


class EducationViewSetTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("user-info")
        cls.user_data = {
            "username": "testuser@abc.com",
            "email": "testuser@abc.com",
            "first_name": "test",
            "last_name": "user",
            "password": "testpassword",
        }
        cls.country = Country.objects.get(label="Turkey")
        cls.profile_data = {
            "country": cls.country,
            "user_type": UserType.objects.get(label="Student"),
            "birth_date": "2000-10-12",
            "description": "lorem ipsum dolor sit amet",
            "profile_picture": "url",
        }
        cls.user = User.objects.create_user(**cls.user_data)
        cls.user_profile = UserProfile.objects.create(user=cls.user, **cls.profile_data)
        cls.token = str(AccessToken.for_user(cls.user))

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.url = reverse("education")

    def test_add_education_success(self):
        education_data = {
            "degree": "2",
            "institution": "2",
            "start_date": "2020-10",
            "end_date": "2021-10",
            "field_of_study": "cs",
        }
        response = self.client.post(self.url, education_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], "success")
        self.assertEqual(response.data["message"], "Education data added successfully")

    def test_update_education_success(self):
        institution = Institution.objects.get(id=2)
        degree = Degree.objects.get(id=2)
        education_data = {
            "degree": degree,
            "institution": institution,
            "start_date": "2020-10",
            "end_date": "2021-10",
            "field_of_study": "cs",
        }
        education = Education.objects.create(
            user_profile=self.user_profile, **education_data
        )
        education_id = education.id
        education_data = {
            "degree": "2",
            "institution": "3",
            "start_date": "2020-10",
            "end_date": "2021-10",
            "field_of_study": "cs",
        }
        response = self.client.put(
            f"/api/user/education/{education_id}/", education_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "success")
        self.assertEqual(response.data["message"], "Education updated successfully")

    def test_delete_education_success(self):
        institution = Institution.objects.get(id=2)
        degree = Degree.objects.get(id=2)
        education_data = {
            "degree": degree,
            "institution": institution,
            "start_date": "2020-10",
            "end_date": "2021-10",
            "field_of_study": "cs",
        }
        education = Education.objects.create(
            user_profile=self.user_profile, **education_data
        )
        education_id = education.id
        response = self.client.delete(f"/api/user/education/{education_id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data["status"], "success")
        self.assertEqual(response.data["message"], "Education deleted successfully")


class UserLoginViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("user-login")
        cls.username = "test@example.com"
        cls.email = "test@example.com"
        cls.password = "testpassword"
        cls.user = User.objects.create_user(
            username=cls.username, email=cls.email, password=cls.password
        )

    def post_request(self, data):
        return self.client.post(self.url, data, format="json")

    def test_user_login_success(self):
        data = {"email": self.email, "password": self.password}
        response = self.post_request(data)

        user = User.objects.get(username=self.username)
        user_object = {
            "user_id": user.id,
            "username": user.username,
            "full_name": f"{user.first_name} {user.last_name}",
            "email": user.email,
        }
        expected_response = {"status": "success", "data": {"user": user_object}}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], expected_response["status"])
        self.assertEqual(
            response.data["data"]["user"], expected_response["data"]["user"]
        )
        self.assertIn("access_token", response.data["data"])

    def test_user_login_invalid_password(self):
        data = {"email": self.email, "password": "invalidpassword"}
        response = self.post_request(data)
        expected_data = {"status": "fail", "message": ["Invalid email or password"]}

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, expected_data)

    def test_user_login_invalid_email(self):
        data = {"email": "wrong@abc.com", "password": self.password}
        response = self.post_request(data)
        expected_data = {"status": "fail", "message": ["Invalid email or password"]}

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, expected_data)

    def test_user_login_invalid_email_format(self):
        data = {"email": "wrong", "password": self.password}
        response = self.post_request(data)
        expected_data = {
            "status": "fail",
            "message": ["Enter a valid email address."],
        }

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_data)

    def test_user_login_missing_fields(self):
        data = {
            "email": self.username,
        }
        response = self.post_request(data)
        expected_data = {
            "status": "fail",
            "message": ["password field is required."],
        }
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_data)

        data = {"password": self.password}
        response = self.post_request(data)
        expected_data = {
            "status": "fail",
            "message": ["email field is required."],
        }
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_data)


class GetUserProfileTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("user-info")
        cls.user_data = {
            "username": "testuser@abc.com",
            "email": "testuser@abc.com",
            "first_name": "test",
            "last_name": "user",
            "password": "testpassword",
        }
        cls.country = Country.objects.get(label="Turkey")
        cls.profile_data = {
            "country": cls.country,
            "user_type": UserType.objects.get(label="Student"),
            "birth_date": "2000-10-12",
            "description": "lorem ipsum dolor sit amet",
            "profile_picture": "url",
        }
        cls.user = User.objects.create_user(**cls.user_data)
        cls.user_profile = UserProfile.objects.create(user=cls.user, **cls.profile_data)
        cls.token = str(AccessToken.for_user(cls.user))

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_get_user_profile_success(self):
        work_data = {
            "position": "Software Engineer",
            "company": "Google",
            "start_date": "2020-10",
            "end_date": "2021-10",
        }
        WorkExperience.objects.create(user_profile=self.user_profile, **work_data)

        education_data = {
            "degree": Degree.objects.get(id=2),
            "institution": Institution.objects.get(id=2),
            "start_date": "2020-01",
            "end_date": "2021-05",
            "field_of_study": "url",
        }
        Education.objects.create(user_profile=self.user_profile, **education_data)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "success")

        self.assertIn("user_id", response.data["data"])
        self.assertIn("username", response.data["data"])
        self.assertIn("email", response.data["data"])
        self.assertIn("description", response.data["data"])
        self.assertIn("profile_picture", response.data["data"])
        self.assertIn("country", response.data["data"])
        self.assertIn("education", response.data["data"])
        self.assertIn("work_experience", response.data["data"])

        self.assertEqual(
            response.data["data"]["education"],
            [
                {
                    "id": 1,
                    "field_of_study": "url",
                    "start_date": "2020-01",
                    "end_date": "2021-05",
                    "user_profile": 1,
                    "institution": 2,
                    "degree": 2,
                }
            ],
        )
        self.assertEqual(
            response.data["data"]["work_experience"],
            [
                {
                    "id": 1,
                    "position": "Software Engineer",
                    "company": "Google",
                    "start_date": "2020-10",
                    "end_date": "2021-10",
                    "profile_picture": None,
                    "user_profile": 1,
                }
            ],
        )

    def test_get_user_profile_with_username(self):
        user_data = {
            "username": "newuser"
        }
        user = User.objects.create_user(**user_data)
        user_profile = UserProfile.objects.create(user=user, **self.profile_data)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer{str(AccessToken.for_user(user))}")
        
        # add username to url
        url = f"{self.url}?username={user.username}"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "success")