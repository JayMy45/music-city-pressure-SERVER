"""View module for handling requests for customer data"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.contrib.auth.models import User
from mcpressureapi.models import ServiceType, Equipment, ServiceTypeEquipment

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
            Response -- JSON serialized service instance
        """
        user = User.objects.get(pk=request.auth.user_id)

        if user.is_staff:

            required_fields = ['name', 'description',
                                'details', 'tool']
            missing_fields = 'You are missing'
            is_fields_missing = False

            for field in required_fields:
                value = request.data.get(field, None)
                if value is None:
                    missing_fields = f'{missing_fields} {field}'
                    is_fields_missing = True
            if is_fields_missing:
                    return Response({"message": missing_fields}, status = status.HTTP_400_BAD_REQUEST)
            
            tool = request.data["tool"]
            for too in tool:
                try:
                    tool_to_assign = Equipment.objects.get(pk=too)
                except Equipment.DoesNotExist:
                    return Response({"message": "The tool you specified does not exist"}, status = status.HTTP_404_NOT_FOUND)


            service = ServiceType.objects.create(
                name = request.data["name"],
                label = request.data["label"],
                description = request.data["description"],
                details = request.data["details"],
                price = request.data["price"]
            )

            for too in tool:
                tool_to_assign = Equipment.objects.get(pk=too)
                service_tool = ServiceTypeEquipment()
                service_tool.equipment_id = tool_to_assign
                service_tool.service_type_id = service
                service_tool.save()


            # new_service.tool = tool
            # new_service.save()
        
        else: 
            return Response({"message": "This function is not available to customers"}, status = status.HTTP_403_FORBIDDEN)
       
        serialized =  ServiceTypeSerializer(service, many=False)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """Handles PUT request of single Service Type

        Return:
            Response - No response body status just (201)
        """ 
        
        try: 
            service = ServiceType.objects.get(pk=pk)
        except ServiceType.DoesNotExist:
            return Response({"message": "The service you specified does not exist"}, status = status.HTTP_404_NOT_FOUND)

        user = User.objects.get(pk=request.auth.user_id)
        if user.is_staff:

            service.name = request.data["name"]
            service.description = request.data["description"]
            service.details = request.data["details"]
            service.price = request.data["price"]
            equipment = Equipment.objects.get(pk=request.data["tool"])
            service.tool = equipment
            
        else:
            return Response({"message": "This function is not available to customers"}, status = status.HTTP_403_FORBIDDEN)

        service.save()
        serialized =  ServiceTypeSerializer(service, many=False)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk):
        try:
            service = ServiceType.objects.get(pk=pk)
            service.delete()
            return Response({"message": "This service has been DELETED"}, status=status.HTTP_204_NO_CONTENT)
        except ServiceType.DoesNotExist:
            return Response({"message": "The service you specified does not exist"}, status = status.HTTP_404_NOT_FOUND)



class ToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ('id', 'label',)

class ServiceTypeSerializer(serializers.ModelSerializer):
    tool = ToolSerializer(many=True)
    class Meta:
        model = ServiceType
        fields = ('id', 'name','description', 'details', 'price', 'tool',)