"""View module for handling requests for customer data"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from mcpressureapi.models import Appointments, Customer, Employee, ServiceType

class AppointmentView(ViewSet):
    """Honey Rae API ServiceTicket view"""
     
    def list(self, request):
        """Handle GET requests to get all customers

        Returns:
            Response -- JSON serialized list of customers
        """

        service_call = Appointments.objects.all()
        serialized = AppointmentsSerializer(service_call, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single customer

        Returns:
            Response -- JSON serialized customer record
        """
        service_call = Appointments.objects.get(pk=pk)
        serialized = AppointmentsSerializer(service_call, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        employee = Employee.objects.get(user=request.auth.user)
        customer = Customer.objects.get(pk=request.data["customer"])
        service_type = ServiceType.objects.get(pk=request.data["service_type"])

        appointment = Appointments.objects.create(
            employee=employee,
            customer=customer,
            service_type=service_type,
            request_date=request.data["request_date"],
            date_completed=request.data["date_completed"],
            consultation= False,
            completed=False,
        )

        serializer = AppointmentsSerializer(appointment)
        return Response(serializer.data)
        
class AppointmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointments
        fields = ('id', 'service_type','completed', 'consultation', )
