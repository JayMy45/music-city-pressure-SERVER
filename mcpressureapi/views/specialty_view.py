"""View module for handling requests for Specialty data"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.contrib.auth.models import User
from mcpressureapi.models import Specialty

class SpecialtyView(ViewSet):
    """Get request to get all Specialties

    Returns:
        Response -- JSON serialized list of Specialties
    """

    def list(self, request):
        """Get request to get all Specialties

        Returns:
            Response -- JSON serialized list of Specialties
        """

        
        specialty = Specialty.objects.all()
        serialized = Specialtyserializer(specialty, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single specialty 

        Returns:
            Response -- JSON serialized specialty
        """

        try:
            specialty = Specialty.objects.get(pk=pk)
        except Specialty.DoesNotExist:
            return Response({"message": "The specialty you specified does not exist"}, status = status.HTTP_404_NOT_FOUND)

        serialized = Specialtyserializer(specialty, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        """Handles PUT request of single specialty

        Return:
            Response - No response body status just (201)
        """
        specialty = Specialty.objects.get(pk=pk)
        specialty.label = request.data['label']


        specialty.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def create(self, request):
        specialty = Specialty.objects.create(
            label = request.data["label"]
        )
        serialized =  Specialtyserializer(specialty, many=False)
        return Response(serialized.data, status=status.HTTP_201_CREATED)


    def destroy(self, request, pk):
        try:
            specialty = Specialty.objects.get(pk=pk)
            specialty.delete()
            return Response({"message": "This specialty has been DELETED"}, status=status.HTTP_204_NO_CONTENT)
        except Specialty.DoesNotExist:
            return Response({"message": "The specialty you specified does not exist"}, status = status.HTTP_404_NOT_FOUND)


class Specialtyserializer(serializers.ModelSerializer):
    class Meta:
        model =  Specialty
        fields = ('id', 'label', )