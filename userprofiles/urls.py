from django.urls import path
from .views import UserRegistrationAPIView, UserProfileViewSet

urlpatterns = [
    path("register/", UserRegistrationAPIView.as_view(), name="user-registration"),
    path(
        "info/",
        UserProfileViewSet.as_view({"post": "create"}),
        name="user-info",
    ),
]
