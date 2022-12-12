"""View module for handling requests for customer data"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.contrib.auth.models import User
from mcpressureapi.models import ServiceType, Equipment

class ServiceTypeView(ViewSet):
    """Music City Pressure API ServiceTicket view"""
     
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

        try:
            service = ServiceType.objects.get(pk=pk)
        except ServiceType.DoesNotExist:
            return Response({"message": "The service you specified does not exist"}, status = status.HTTP_404_NOT_FOUND)

        serialized = ServiceTypeSerializer(service, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Handle POST request for Service Types

        Returns:
            Response -- JSON serialized appointment instance
        """
        user = User.objects.get(pk=request.auth.user_id)

        if user.is_staff:

            required_fields = ['name', 'description',
                                'details', 'equipment_id']
            missing_fields = 'You are missing'
            is_fields_missing = False

            for field in required_fields:
                value = request.data.get(field, None)
                if value is None:
                    missing_fields = f'{missing_fields} {field}'
                    is_fields_missing = True
            if is_fields_missing:
                    return Response({"message": missing_fields}, status = status.HTTP_400_BAD_REQUEST)

            new_service = ServiceType()
            new_service.name = request.data["name"]
            new_service.label = request.data["label"]
            new_service.description = request.data["description"]
            new_service.details = request.data["details"]
            new_service.price = request.data["price"]

            equipment_id = Equipment.objects.get(pk=request.data["equipment_id"])
            new_service.equipment_id = equipment_id
            new_service.save()
        
        else: 
            return Response({"message": "This function is not available to customers"}, status = status.HTTP_403_FORBIDDEN)
       
        serialized =  ServiceTypeSerializer(new_service, many=False)
        return Response(serialized.data, status=status.HTTP_201_CREATED)


class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = ('id', 'name','description', 'details',)