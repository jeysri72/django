# Import generics to use pre-built views for common API operations (List, Create, Retrieve, Update, Destroy)
from rest_framework import generics 

# Import the Profile model to define the queryset for the views
from .models import Profile 

# Import the ProfileSerializer to handle data validation and serialization
from .serializers import ProfileSerializer 

# A view to handle both listing all Profile objects (GET) and creating a new Profile (POST)
class ProfileListCreateView(generics.ListCreateAPIView): 
    queryset = Profile.objects.all()  # Fetches all Profile objects from the database
    serializer_class = ProfileSerializer  # Uses ProfileSerializer to validate and serialize data

# A view to handle retrieving (GET), updating (PUT/PATCH), and deleting (DELETE) a single Profile object
class ProfileRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView): 
    queryset = Profile.objects.all()  # Fetches all Profile objects, filtered later by primary key (pk)
    serializer_class = ProfileSerializer  # Uses ProfileSerializer to validate and serialize data
