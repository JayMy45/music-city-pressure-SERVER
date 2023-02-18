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

    
    def create(self, request):
        city_pk = request.data["city"]
        try:
            city_instance = City.objects.get(pk=city_pk)
        except City.DoesNotExist:
            # If the city doesn't exist, create a new City instance
            city_instance = City.objects.create(pk=city_pk)

        location = Location.objects.create(
            street=request.data["street"],
            city=city_instance
        )
        serialized = LocationSerializer(location, many=False)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    
    def destroy(self, request, pk):
        """Handle DELETE request for locations

           Returns:
            Response -- "message": "This location has been DELETED"} and status=status.HTTP_204_NO_CONTENT
        """

        try:
            location = Location.objects.get(pk=pk)
            location.delete()
            return Response({"message": "This location has been DELETED"}, status=status.HTTP_204_NO_CONTENT)
        except Location.DoesNotExist:
            return Response({"message": "The location you specified does not exist"}, status = status.HTTP_404_NOT_FOUND)


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name',)

class LocationSerializer(serializers.ModelSerializer):
    city = CitySerializer(many=False)
    class Meta:
        model = Location
        fields = ('id', 'street', 'city',)