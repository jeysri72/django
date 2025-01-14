# Import necessary modules
from rest_framework.views import APIView  # Add this import for APIView
from .models import Profile  # Import the Profile model to interact with the database
from .serializers import ProfileSerializer  # Import the ProfileSerializer to convert the Profile model into JSON format
from rest_framework.response import Response  # Import the Response class to return HTTP responses
from rest_framework.exceptions import NotFound  # Import the NotFound exception to handle missing objects
from rest_framework import status  # Import HTTP status codes for response statuses



# Ref: https://www.django-rest-framework.org/api-guide/viewsets/


# Class-based view to list all profiles
class ProfileListView(APIView):
    # GET request handler
    def get(self, request):
        Profiles = Profile.objects.all()  # Retrieve all Profile objects from the database
        serializer = ProfileSerializer(Profiles, many=True)  # Serialize the queryset into JSON format
        return Response(serializer.data, status=status.HTTP_200_OK)  # Return the serialized data as a response with status 200 OK

# Class-based view to create a new profile
class ProfileCreateView(APIView):
    # POST request handler
    def post(self, request):
        serializer = ProfileSerializer(data=request.data)  # Deserialize the incoming data into a ProfileSerializer instance
        if serializer.is_valid():  # Check if the serializer data is valid
            serializer.save()  # Save the new Profile object into the database
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Return the created data with status 201 CREATED
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return errors with status 400 if validation fails
    
# Class-based view to retrieve details of a specific profile
class ProfileDetailView(APIView):
    # Helper method to get the Profile object by its primary key (pk)
    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)  # Try to get the profile by its primary key
        except Profile.DoesNotExist:  # If the profile doesn't exist, raise a NotFound exception
            raise NotFound("Profile not found.")

    # GET request handler for retrieving a specific profile by pk
    def get(self, request, pk):
        Profile = self.get_object(pk)  # Retrieve the Profile object using the helper method
        serializer = ProfileSerializer(Profile)  # Serialize the Profile object into JSON
        return Response(serializer.data)  # Return the serialized data as a response

# Class-based view to update an existing profile
class ProfileUpdateView(APIView):
    # Helper method to get the Profile object by its primary key (pk)
    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)  # Try to get the profile by its primary key
        except Profile.DoesNotExist:  # If the profile doesn't exist, raise a NotFound exception
            raise NotFound("Profile not found.")

    # PUT request handler for updating a profile by pk
    def put(self, request, pk):
        Profile = self.get_object(pk)  # Retrieve the Profile object using the helper method
        serializer = ProfileSerializer(Profile, data=request.data, partial=True)  # Deserialize the updated data
        if serializer.is_valid():  # Check if the updated data is valid
            serializer.save()  # Save the updated profile back to the database
            return Response(serializer.data)  # Return the updated profile data as a response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return errors with status 400 if validation fails

# Class-based view to delete a profile
class ProfileDeleteView(APIView):
    # Helper method to get the Profile object by its primary key (pk)
    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)  # Try to get the profile by its primary key
        except Profile.DoesNotExist:  # If the profile doesn't exist, raise a NotFound exception
            raise NotFound("Profile not found.")

    # DELETE request handler for deleting a profile by pk
    def delete(self, request, pk):
        Profile = self.get_object(pk)  # Retrieve the Profile object using the helper method
        Profile.delete()  # Delete the Profile object from the database
        return Response(status=status.HTTP_204_NO_CONTENT)  # Return an empty response with status 204 NO CONTENT (successful deletion)
