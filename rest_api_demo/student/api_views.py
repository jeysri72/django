# views.py

# Ref: https://www.django-rest-framework.org/api-guide/viewsets/

from rest_framework import viewsets  # Import the viewsets module to create RESTful views

from .models import Profile  # Import the Profile model to interact with the database
from .serializers import ProfileSerializer  # Import the ProfileSerializer for data serialization and deserialization

# Define a ViewSet for the Profile model
class ProfileViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for handling CRUD operations on the Profile model.
    Inherits from ModelViewSet, which provides default implementations
    for create, retrieve, update, partial_update, destroy, and list actions.
    """
    queryset = Profile.objects.all()  # Define the queryset to include all Profile objects
    serializer_class = ProfileSerializer  # Specify the serializer class to handle Profile instances


