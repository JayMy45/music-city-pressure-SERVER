"""View module for handling requests for customer data"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from mcpressureapi.models import ServiceCall

class ServiceCallView(ViewSet):
    """Honey Rae API ServiceTicket view"""
     
    def list(self, request):
        """Handle GET requests to get all customers

        Returns:
            Response -- JSON serialized list of customers
        """

        service_call = ServiceCall.objects.all()
        serialized = ServiceCallSerializer(service_call, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single customer

        Returns:
            Response -- JSON serialized customer record
        """
        service_call = ServiceCall.objects.get(pk=pk)
        serialized = ServiceCallSerializer(service_call, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)
        
class ServiceCallSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCall
        fields = ('id', 'completed', )
