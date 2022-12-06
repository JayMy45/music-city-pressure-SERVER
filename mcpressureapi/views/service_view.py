"""View module for handling requests for customer data"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from mcpressureapi.models import ServiceType

class ServiceTypeView(ViewSet):
    """Honey Rae API ServiceTicket view"""
     
    def list(self, request):
        """Handle GET requests to get all customers

        Returns:
            Response -- JSON serialized list of customers
        """

        service = ServiceType.objects.all()
        serialized = ServiceTypeSerializer(service, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)


class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = ('id', 'label',)