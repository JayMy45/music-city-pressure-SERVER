"""View module for handling requests for Employee data"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from django.contrib.auth.models import User
from mcpressureapi.models import Employee, Specialty

class EmployeeView(ViewSet):
    """Get request to get all Employees

    Returns:
        Response -- JSON serialized list of Employees
    """

    @action(methods=['get'], detail=False)
    def current_employee(self,request):
        """Get current logged in Employee"""
        employee = Employee.objects.get(user=request.auth.user)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        """Get request to get all Employees

        Returns:
            Response -- JSON serialized list of Employees
        """
        # user = User.objects.get(pk=request.auth.user_id)
        # if user.is_staff:
        employee = Employee.objects.all()

        # else: 
        #     return Response(serialized.data, status=status.HTTP_401_UNAUTHORIZED)

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
        employee.image = request.data['image']

        employee.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        try:
            service = Employee.objects.get(pk=pk)
            service.delete()
            return Response({"message": "This service has been DELETED"}, status=status.HTTP_204_NO_CONTENT)
        except Employee.DoesNotExist:
            return Response({"message": "The service you specified does not exist"}, status = status.HTTP_404_NOT_FOUND)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model =  User
        fields = ('id','is_staff', 'is_superuser', 'first_name', 'email', )

class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model =  Specialty
        fields = ('id','label', )

class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    specialty = SpecialtySerializer(many=True)
    class Meta:
        model =  Employee
        fields = ('id','full_name', 'address', 'phone_number', 'bio', 
                  'salary', 'user', 'specialty', 'image',  )