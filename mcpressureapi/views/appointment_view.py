"""View module for handling requests for customer data"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.contrib.auth.models import User
from mcpressureapi.models import Appointments, Customer, Employee, ServiceType

class AppointmentView(ViewSet):
    """Music City Pressure API Appointment view"""
     
    def list(self, request):
        """Handle GET requests to get all Appointments

        Returns:
            Response -- JSON serialized list of appointments
        """

        appointments = Appointments.objects.all()
        serialized = AppointmentsSerializer(appointments, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single Appointment

        Returns:
            Response -- JSON serialized appointment record
        """
        appointment = Appointments.objects.get(pk=pk)
        serialized = AppointmentsSerializer(appointment, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        
        # if employee is creating an appointment then the employee will be assigned to the that appt.
        user = User.objects.get(pk=request.auth.user_id)
        if user.is_staff:
            employee = Employee.objects.get(user=request.auth.user)
            customer = Customer.objects.get(pk=request.data["customer"])
            service_type = ServiceType.objects.get(pk=request.data["service_type"])

            appointment = Appointments.objects.create(
                employee=employee,
                customer=customer,
                service_type=service_type,
                request_date=request.data["request_date"],
                request_details=request.data["request_details"],
                consultation= False,
                completed=False,
            )
        # if customer is creating an appointment then an employee wont be assigned
        else:
            customer = Customer.objects.get(user=request.auth.user)
            service_type = ServiceType.objects.get(pk=request.data["service_type"])

            appointment = Appointments.objects.create(
                customer=customer,
                service_type=service_type,
                request_date=request.data["request_date"],
                request_details=request.data["request_details"],
                consultation= False,
                completed=False,
            )
    
        

        serializer = AppointmentsSerializer(appointment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        



class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'full_name',)

class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = ('id', 'name','description',)

class AppointmentsSerializer(serializers.ModelSerializer):
    service_type = ServiceTypeSerializer(many=False)
    customer = CustomerSerializer(many=False)
    class Meta:
        model = Appointments
        fields = ('id', 'service_type','completed', 'consultation', 'request_details', 'request_date', 'customer' )
