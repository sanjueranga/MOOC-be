from django.urls import path
from .views import UserRegistrationAPIView, UserProfileViewSet, WorkExperienceViewset, EducationViewset,UserLoginApiView

urlpatterns = [
    path("register/", UserRegistrationAPIView.as_view(), name="user-registration"),
    path("login/", UserLoginApiView.as_view(), name="user-login"),
    path(
        "info/",
        UserProfileViewSet.as_view({"post": "create", "put": "update","get": "list"}),
        name="user-info",
    ),
    path(
        "work/",
        WorkExperienceViewset.as_view({"post": "create", "get": "list"}),
        name="work-experience",
    ),
    path(
        "work/<int:pk>/",
        WorkExperienceViewset.as_view({"put": "update", "delete": "destroy"}),
        name="work-experience",
    ),
    path(
        "education/",
        EducationViewset.as_view({"post": "create","get": "list"}),
        name="education",
    ),
    path(
        "education/<int:pk>/",
        EducationViewset.as_view({"put": "update", "delete": "destroy"}),
        name="education",
    ),
]
