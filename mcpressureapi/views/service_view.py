"""View module for handling requests for customer data"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from mcpressureapi.models import ServiceType

class ServiceTypeView(ViewSet):
    """Honey Rae API ServiceTicket view"""
     
    def list(self, request):
        """Handle GET requests to get all services

        Returns:
            Response -- JSON serialized list of services
        """

        service = ServiceType.objects.all()
        serialized = ServiceTypeSerializer(service, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single service 

        Returns:
            Response -- JSON serialized service
        """
        service = ServiceType.objects.get(pk=pk)
        serialized = ServiceTypeSerializer(service, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)



class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = ('id', 'name','description', 'details',)