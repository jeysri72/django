from django.urls import path
from .api_views import ProfileListCreateView, ProfileRetrieveUpdateDestroyView

urlpatterns = [
    # URL for listing all profiles or creating a new profile
    path('profiles/', ProfileListCreateView.as_view(), name='profile-list-create'),
    
    # URL for retrieving, updating, or deleting a specific profile by its primary key (pk)
    path('profiles/<int:pk>/', ProfileRetrieveUpdateDestroyView.as_view(), name='profile-detail'),
]
