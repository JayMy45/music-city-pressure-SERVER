from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.contrib.auth.models import User
from mcpressureapi.models import Employee

class EmployeeView(ViewSet):
    """Get request to get all Employees

    Returns:
        Response -- JSON serialized list of Employees
    """

    def list(self, request):
        """Get request to get all Employees

        Returns:
            Response -- JSON serialized list of Employees
        """

        
        employee = Employee.objects.all()
        serialized = EmployeeSerializer(employee, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model =  User
        fields = ('id','is_staff', )

class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model =  Employee
        fields = ('id','full_name', 'address', 'phone_number', 'user', )