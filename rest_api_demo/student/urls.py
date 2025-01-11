# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import ProfileViewSet

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]


