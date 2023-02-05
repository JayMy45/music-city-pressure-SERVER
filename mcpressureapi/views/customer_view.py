from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from django.contrib.auth.models import User
from mcpressureapi.models import Customer, City, Location

class CustomerView(ViewSet):
    """Get request to get all Customers

    Returns:
        Response -- JSON serialized list of Customers
    """

    @action(methods=['get'], detail=False)
    def current_customer(self,request):
        """Get current logged in Customer"""
        try:
            customer = Customer.objects.get(user=request.auth.user)
        except:
            user = User.objects.get(pk=request.auth.user_id)
            if user.is_staff:
                pass

        serializer = CustomerSerializer(customer)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def list(self, request):
        """Get request to get all Customers

        Returns:
            Response -- JSON serialized list of Customers
        """
        user = User.objects.get(pk=request.auth.user_id)
        if user.is_staff:
            customer = Customer.objects.all().order_by('user__first_name', 'user__last_name')

            
        else:
            log_customer =  Customer.objects.get(user=request.auth.user)
            customer = Customer.objects.filter(user_id= log_customer.user_id)
            
        serialized = CustomerSerializer(customer, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single customer 

        Returns:
            Response -- JSON serialized customer
        """

        try:
            customer = Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            return Response({"message": "The customer you specified does not exist"}, status = status.HTTP_404_NOT_FOUND)

        serialized = CustomerSerializer(customer, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model =  User
        fields = ('id','is_staff', 'email',)

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name',)

class LocationSerializer(serializers.ModelSerializer):
    city = CitySerializer(many=False)
    class Meta:
        model = Location
        fields = ('id', 'street', 'city',)

class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    location = LocationSerializer(many=True)
    full_name = serializers.ReadOnlyField()
    class Meta:
        model =  Customer
        fields = ('id','full_name', 'address', 'location', 'phone_number', 'user', )