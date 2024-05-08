from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet

router = DefaultRouter()
router.register(r"", CourseViewSet, basename="course")

urlpatterns = []
urlpatterns = router.urls + urlpatterns
