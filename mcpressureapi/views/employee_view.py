"""View module for handling requests for Employee data"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from django.contrib.auth.models import User
from mcpressureapi.models import Employee, Specialty, EmployeeServiceTypeSpecialty

class EmployeeView(ViewSet):
    """Get request to get all Employees

    Returns:
        Response -- JSON serialized list of Employees
    """

    @action(methods=['get'], detail=False)
    def current_employee(self,request):
        """Get current logged in Employee"""
        # user = User.objects.get(pk=request.auth.user_id)
        # if user.is_staff:
        employee = Employee.objects.get(user=request.auth.user)

        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)

#* Remove specialty Employee Method
# action decorator accepts delete request (methods=['delete]) and a detail route (detail=True)
    @action(methods=['delete'], detail=True)
    def remove_specialty(self, request, pk):
        """DELETE request for a Admin to remove_specialty an from Employee details"""
        #retrieves specialty primary keys to remove_specialty from request data
        specialty_pks = request.data.get("specialty_pks")
        #retrieves employee by primary key
        employee = Employee.objects.get(pk=pk)
        for specialty_pk in specialty_pks:
            #retrieves specialty by primary key
            skill = Specialty.objects.filter(pk=specialty_pk).first()
            # check if specialty exists or not
            if skill is None:
                # returns a 404 status with a message if specialty does not exist
                return Response({'message': f'Specialty {specialty_pk} does not exist'}, status=status.HTTP_404_NOT_FOUND)
            #removes specialty from join table
            EmployeeServiceTypeSpecialty.objects.filter(specialty=skill, employee=employee).delete()
        # returns 200 status and message 
        return Response({'message':'Specialty has been removed from Employee'}, status=status.HTTP_200_OK)



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

        specialties = request.data.get("specialty", None)

        employee = Employee.objects.get(pk=pk)
        employee.bio = request.data['bio']
        employee.address = request.data['address']
        employee.phone_number = request.data['phone_number']
        employee.salary = request.data['salary']
        employee.image = request.data['image']

        employee.save()

        if specialties is not None:
                for specialty in specialties:
                    specialty_to_assign = Specialty.objects.get(pk=specialty)
                    employee_specialty = EmployeeServiceTypeSpecialty()
                    employee_specialty.specialty = specialty_to_assign
                    employee_specialty.employee = employee
                    employee_specialty.save()

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
        fields = ('id','is_staff', 'is_superuser', 'first_name', 'last_name', 'email', )

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