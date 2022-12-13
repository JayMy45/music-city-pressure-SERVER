from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.contrib.auth.models import User
from mcpressureapi.models import Equipment

class EquipmentView(ViewSet):
    """Get request to get all Equipments

    Returns:
        Response -- JSON serialized list of Equipments
    """

    def list(self, request):
        """Get request to get all Equipments

        Returns:
            Response -- JSON serialized list of Equipments
        """
        
        equipment = Equipment.objects.all()
        serialized = EquipmentSerializer(equipment, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        """Handle GET requests for single equipment 

        Returns:
            Response -- JSON serialized equipment
        """

        try:
            equipment = Equipment.objects.get(pk=pk)
        except Equipment.DoesNotExist:
            return Response({"message": "The equipment you specified does not exist"}, status = status.HTTP_404_NOT_FOUND)

        serialized = EquipmentSerializer(equipment, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Equipment
        fields = ('id','label', )
