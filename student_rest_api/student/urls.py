# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from .views import ProfileViewSet

# router = DefaultRouter()
# router.register(r'profiles', ProfileViewSet)

# urlpatterns = [
#     path('', include(router.urls)),
# ]



from .api_views import (
    ProfileListView,
    ProfileCreateView,
    ProfileDetailView,
    ProfileUpdateView,
    ProfileDeleteView,
)

urlpatterns = [
    path('api/v1/profiles/', ProfileListView.as_view(), name='profile-list'),
    path('api/v1/profiles/create/', ProfileCreateView.as_view(), name='profile-create'),
    path('api/v1/profiles/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('api/v1/profiles/<int:pk>/update/', ProfileUpdateView.as_view(), name='profile-update'),
    path('api/v1/profiles/<int:pk>/delete/', ProfileDeleteView.as_view(), name='profile-delete'),
]


