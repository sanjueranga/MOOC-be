from django.urls import path
from .views import UserRegistrationAPIView, UserProfileViewSet, WorkExperienceViewset

urlpatterns = [
    path("register/", UserRegistrationAPIView.as_view(), name="user-registration"),
    path(
        "info/",
        UserProfileViewSet.as_view({"post": "create", "put": "update"}),
        name="user-info",
    ),
    path(
        "work/",
        WorkExperienceViewset.as_view({"post": "create","get": "list"}),
        name="work-experience",
    ),
    path(
        "work/<int:pk>/",
        WorkExperienceViewset.as_view({"put": "update", "delete": "destroy"}),
        name="work-experience",
    ),
]
