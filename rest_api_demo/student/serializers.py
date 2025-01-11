# serializers.py 

from rest_framework import serializers  # Import the serializers module from Django REST Framework
from .models import Profile  # Import the Profile model from the current app's models

# Define a serializer for the Profile model
class ProfileSerializer(serializers.ModelSerializer):
    # Meta class defines metadata for the serializer
    class Meta:
        model = Profile  # Specify the model to serialize
        fields = ['id', 'first_name', 'last_name', 'email']  # Fields to include in the serialization

    # Custom validation method for the 'email' field
    def validate_email(self, value):
        """
        Check if the email is unique in the Profile model.
        If the email already exists, raise a ValidationError.
        """
        if Profile.objects.filter(email=value).exists():  # Check if a Profile with this email already exists
            raise serializers.ValidationError("A student with this email already exists.")  # Raise error if not unique
        return value  # Return the value if it's unique
