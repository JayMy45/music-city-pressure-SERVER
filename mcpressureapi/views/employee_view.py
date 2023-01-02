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

    def retrieve(self, request, pk=None):
        """Handle GET requests for single employee 

        Returns:
            Response -- JSON serialized employee
        """

        try:
            employee = Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            return Response({"message": "The employee you specified does not exist"}, status = status.HTTP_404_NOT_FOUND)

        serialized = EmployeeSerializer(employee, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        """Handles PUT request of single employee

        Return:
            Response - No response body status just (201)
        """
        employee = Employee.objects.get(pk=pk)
        employee.bio = request.data['bio']
        employee.address = request.data['address']
        employee.phone_number = request.data['phone_number']
        employee.salary = request.data['salary']

        employee.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model =  User
        fields = ('id','is_staff', "is_superuser" )

class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model =  Employee
        fields = ('id','full_name', 'address', 'phone_number', 'bio', 
                  'salary', 'user',)