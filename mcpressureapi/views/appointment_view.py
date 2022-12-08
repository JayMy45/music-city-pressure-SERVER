"""View module for handling requests for customer data"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.contrib.auth.models import User
from mcpressureapi.models import Appointments, Customer, Employee, ServiceType, Progress

class AppointmentView(ViewSet):
    """Music City Pressure API Appointment view"""
     
    def list(self, request):
        """Handle GET requests to get all Appointments

        Returns:
            Response -- JSON serialized list of appointments
        """

        user = User.objects.get(pk=request.auth.user_id)

        # determine if user is_staff/employee
        if user.is_staff:
            # get all appointments
            appointments = Appointments.objects.all()

        else:
            # filter appointments according to logged in customer
            log_user = Customer.objects.get(user=request.auth.user)
            appointments = Appointments.objects.filter(customer_id = log_user)


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
        
        user = User.objects.get(pk=request.auth.user_id)

        # determine if user is_staff/employee
        if user.is_staff:

            # if employee is creating an appointment then the employee will be assigned to the that appt.
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

        else:

            customer = Customer.objects.get(user=request.auth.user)
            service_type = ServiceType.objects.get(pk=request.data["service_type"])

            # if customer is creating an appointment then without assigned employee
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

    def update(self, request, pk=None):
        """Handles PUT request of single customer

        Return:
            Response - No response body status just (204)
        """

        user = User.objects.get(pk=request.auth.user_id)
        appointment = Appointments.objects.get(pk=pk)

        # determine if user is_staff/employee
        if user.is_staff:

            # if staff is updating appointment
            service_type = ServiceType.objects.get(pk=request.data["service_type"])
            appointment.service_type = service_type
            progress = Progress.objects.get(pk=request.data["progress"])
            appointment.progress = progress
            appointment.service_type = service_type
            appointment.request_date = request.data["request_date"]
            appointment.date_completed = request.data["date_completed"]
            appointment.consultation = request.data["consultation"]
            appointment.completed = request.data["completed"]
        
        else:
            
            # if customer is updating an appointment   
            service_type = ServiceType.objects.get(pk=request.data["service_type"])
            appointment.service_type = service_type
            appointment.request_date = request.data["request_date"]
            appointment.consultation = request.data["consultation"]
            appointment.completed = request.data["completed"]
            appointment.request_details = request.data["request_details"]
            

        appointment.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


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
