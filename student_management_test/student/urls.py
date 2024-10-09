from django.urls import path
from . import views # Import views from the current app

app_name = 'student'  # This defines the namespace



urlpatterns = [

    #landing page 
    path('', views.home, name='home'),
    
    # List all profiles
    path('profiles', views.profile_list, name='profile_list'),

    # View a profile
    path('profiles/<int:pk>/', views.profile_detail, name='profile_detail'),

    # Create a new profile
    path('profiles/create/', views.profile_create, name='profile_create'),

    # Update an existing profile (with primary key passed as argument)
    path('profiles/update/<int:pk>/', views.profile_update, name='profile_update'),

    # Delete a profile (with primary key passed as argument)
    path('profiles/delete/<int:pk>/', views.profile_delete, name='profile_delete'),


]