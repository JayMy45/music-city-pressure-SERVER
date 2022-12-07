from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from mcpressureapi.models import Customer

class CustomerView(ViewSet):
    """Get request to get all Customers

    Returns:
        Response -- JSON serialized list of Customers
    """

    def list(self, request):
        """Get request to get all Customers

        Returns:
            Response -- JSON serialized list of Customers
        """

        customer = Customer.objects.all()
        serialized = CustomerSerializer(customer, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Customer
        fields = ('id','full_name', 'address', 'phone_number', )