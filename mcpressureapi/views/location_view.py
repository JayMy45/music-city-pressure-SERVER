"""View module for handling requests for Location data"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from mcpressureapi.models import Location, City


class LocationView(ViewSet):
    """Music City Pressure API Location view"""

    def list(self, request):
        """Handle GET requests to get all locations

        Returns:
            Response -- JSON serialized list of locations
        """
     
        location = Location.objects.all()
        serialized = LocationSerializer(location, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)


    def retrieve(self, request, pk=None):
            """Handle GET requests for single location 

            Returns:
                Response -- JSON serialized location
            """

            try:
                location = Location.objects.get(pk=pk)
            except Location.DoesNotExist:
                return Response({"message": "The location you specified does not exist"}, status = status.HTTP_404_NOT_FOUND)

            serialized = LocationSerializer(location, context={'request': request})
            return Response(serialized.data, status=status.HTTP_200_OK)

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name',)

class LocationSerializer(serializers.ModelSerializer):
    city = CitySerializer(many=False)
    class Meta:
        model = Location
        fields = ('id', 'street', 'city',)