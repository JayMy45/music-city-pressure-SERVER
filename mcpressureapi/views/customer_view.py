from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.contrib.auth.models import User
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

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model =  User
        fields = ('id','is_staff', )


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model =  Customer
        fields = ('id','full_name', 'address', 'phone_number', 'user', )