"""View module for handling requests for City data"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from mcpressureapi.models import City


class CityView(ViewSet):
    """Music City Pressure API City view"""

    def list(self, request):
        """Handle GET requests to get all cities

        Returns:
            Response -- JSON serialized list of cities
        """
     
        city = City.objects.all()
        serialized = CitySerializer(city, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name',)