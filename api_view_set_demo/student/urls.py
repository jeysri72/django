from django.urls import path
from . import api_views  # Import the views from api_views.py

urlpatterns = [
    # URL pattern for listing profiles
    path('profiles/', api_views.ProfileListView.as_view(), name='profile-list'),
    
    # URL pattern for creating a new profile
    path('profiles/create/', api_views.ProfileCreateView.as_view(), name='profile-create'),
    
    # URL pattern for viewing a specific profile's details
    path('profiles/<int:pk>/', api_views.ProfileDetailView.as_view(), name='profile-detail'),
    
    # URL pattern for updating a specific profile
    path('profiles/<int:pk>/update/', api_views.ProfileUpdateView.as_view(), name='profile-update'),
    
    # URL pattern for deleting a specific profile
    path('profiles/<int:pk>/delete/', api_views.ProfileDeleteView.as_view(), name='profile-delete'),
]
