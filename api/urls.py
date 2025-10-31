from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet

app_name = 'api'

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
