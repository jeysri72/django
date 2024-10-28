# views.py

# Ref: https://www.django-rest-framework.org/api-guide/viewsets/

from rest_framework import viewsets
from rest_framework.views import APIView

from rest_framework import status
from .models import Profile
from .serializers import ProfileSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from rest_framework.exceptions import NotFound


# class ProfileViewSet(viewsets.ModelViewSet):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer


class ProfileListView(APIView):
    def get(self, request):
        Profiles = Profile.objects.all()
        serializer = ProfileSerializer(Profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProfileCreateView(APIView):
    def post(self, request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProfileDetailView(APIView):
    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise NotFound("Profile not found.")

    def get(self, request, pk):
        Profile = self.get_object(pk)
        serializer = ProfileSerializer(Profile)
        return Response(serializer.data)


class ProfileUpdateView(APIView):
    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise NotFound("Profile not found.")

    def put(self, request, pk):
        Profile = self.get_object(pk)
        serializer = ProfileSerializer(Profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ProfileDeleteView(APIView):
    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise NotFound("Profile not found.")

    def delete(self, request, pk):
        Profile = self.get_object(pk)
        Profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
