"""View module for handling requests for customer data"""
from django.http import HttpResponseServerError
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.contrib.auth.models import User
from mcpressureapi.models import Appointments, Customer, Employee, ServiceType, Progress, EmployeeAppointment

class AppointmentView(ViewSet):
    """Music City Pressure API Appointment view"""

    #Unassign Employee Method
# action decorator accepts delete request (methods=['delete]) and a detail route (detail=True)
    @action(methods=['delete'], detail=True)
    def unassign(self, request, pk):
        """DELETE request for a user to unassign an employee from an event"""
        employee_pks = request.data.get("employee_pks")
        appointment = Appointments.objects.get(pk=pk)
        for employee_pk in employee_pks:
            technician = Employee.objects.filter(pk=employee_pk).first()
            if technician is None:
                return Response({'message': f'Employee {employee_pk} does not exist'}, status=status.HTTP_404_NOT_FOUND)
            #removes employee from join table
            EmployeeAppointment.objects.filter(employee=technician, appointment=appointment).delete()
        # returns 200 status and message 
        return Response({'message':'Employees has left the appointment'}, status=status.HTTP_200_OK)

    
    def list(self, request):
        """Handle GET requests to get all Appointments

        Returns:
            Response -- JSON serialized list of appointments
        """

        # user = User.objects.get(pk=request.auth.user_id)
        try: 
            log_user = Customer.objects.get(user=request.auth.user)

            if log_user:
                appointments = Appointments.objects.filter(customer_id = log_user)

        except:
            # user.is_staff
            # get all appointments
            appointments = Appointments.objects.all()
            
        serialized = AppointmentsSerializer(appointments, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single Appointment

        Returns:
            Response -- JSON serialized appointment record
        """
        try:
            appointment = Appointments.objects.get(pk=pk)

        except Appointments.DoesNotExist:
            return Response({"message": "The appointment you specified does not exist"}, status = status.HTTP_404_NOT_FOUND)

        serialized = AppointmentsSerializer(appointment, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)


    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized appointment instance
        """
        
        user = User.objects.get(pk=request.auth.user_id)

        # determine if user is_staff/employee
        if user.is_staff:

            required_fields = ['service_type', 'request_date',
                               'completed']
            missing_fields = 'You are missing'
            is_fields_missing = False

            for field in required_fields:
                value = request.data.get(field, None)
                if value is None:
                    missing_fields = f'{missing_fields} {field}'
                    is_fields_missing = True
            if is_fields_missing:
                    return Response({"message": missing_fields}, status = status.HTTP_400_BAD_REQUEST)

            # if employee is creating an appointment then the employee will be assigned to the that appt.
            
            employees = request.data.get("employee", None)

            customer = Customer.objects.get(pk=request.data["customer"])
            service_type = ServiceType.objects.get(pk=request.data["service_type"])
            progress = Progress.objects.get(pk=request.data["progress"])

            appointment = Appointments.objects.create(
                customer=customer,
                service_type=service_type,
                request_details=request.data["request_details"],
                request_date=request.data["request_date"],
                image=request.data["image"],
                progress = progress,
                scheduled = False,
                consultation= False,
                completed=False,
                confirm=False,
            )

            if employees is not None:
                for employee in employees:
                    employees_to_assign = Employee.objects.get(pk=employee)
                    employee_appointment = EmployeeAppointment()
                    employee_appointment.employee = employees_to_assign
                    employee_appointment.appointment = appointment
                    employee_appointment.save()

        else:

            required_fields = ['service_type', 'request_date']
            missing_fields = 'You are missing'
            is_fields_missing = False

            for field in required_fields:
                value = request.data.get(field, None)
                if value is None:
                    missing_fields = f'{missing_fields} {field}'
                    is_fields_missing = True
            if is_fields_missing:
                    return Response({"message": missing_fields}, status = status.HTTP_400_BAD_REQUEST)

            customer = Customer.objects.get(user=request.auth.user)
            service_type = ServiceType.objects.get(pk=request.data["service_type"])
            progress = Progress.objects.get(pk=request.data["progress"])

            # if customer is creating an appointment then without assigned employee
            appointment = Appointments.objects.create(
                customer=customer,
                service_type=service_type,
                request_date=request.data["request_date"],
                request_details=request.data["request_details"],
                image=request.data["image"],
                scheduled = False,
                progress = progress,
                consultation= False,
                completed=False,
            )


    
        serializer = AppointmentsSerializer(appointment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """Handles PUT request of single customer

        Return:
            Response - No response body just message and status (201, 204, 400)
        """ 

        user = User.objects.get(pk=request.auth.user_id)
        
        try:
            appointment = Appointments.objects.get(pk=pk)

        except Appointments.DoesNotExist:
            return Response({"message": "The appointment you specified does not exist"}, status = status.HTTP_404_NOT_FOUND)


        # determine if user is_staff/employee
        if user.is_staff:
            # determine if data is missing from PUT request (staff)
            required_fields = ['service_type','progress',
                            'request_date',
                            'consultation','completed']
            missing_fields = 'You are missing'
            is_fields_missing = False

            for field in required_fields:
                value = request.data.get(field, None)
                if value is None:
                    missing_fields = f'{missing_fields} {field}'
                    is_fields_missing = True
            if is_fields_missing:
                    return Response({"message": missing_fields}, status = status.HTTP_400_BAD_REQUEST)

            
            employees = request.data.get("employee", None)
            request_details = request.data.get("request_details", None)
            image = request.data.get("image", None)

            # if staff is updating appointment
            service_type = ServiceType.objects.get(pk=request.data["service_type"])
            appointment.service_type = service_type
            progress = Progress.objects.get(pk=request.data["progress"])
            appointment.progress = progress
            appointment.request_date = request.data["request_date"]
            appointment.scheduled = request.data["scheduled"]
            appointment.confirm = request.data["confirm"]
            appointment.consultation = request.data["consultation"]
            appointment.completed = request.data["completed"]

            if request_details is not None:
                appointment.request_details = request.data["request_details"]

            if image is not None:
                appointment.image = request.data["image"]


            
            appointment.save()

            if employees is not None:
                for employee in employees:
                    employees_to_assign = Employee.objects.get(pk=employee)
                    employee_appointment = EmployeeAppointment()
                    employee_appointment.employee = employees_to_assign
                    employee_appointment.appointment = appointment
                    employee_appointment.save()
        
        else:
            # determine if data is missing from PUT request (customer)
            required_fields = ['service_type', 'request_date']
            missing_fields = 'You are missing'
            is_fields_missing = False

            for field in required_fields:
                value = request.data.get(field, None)
                if value is None:
                    missing_fields = f'{missing_fields} {field}'
                    is_fields_missing = True
            if is_fields_missing:
                    return Response({"message": missing_fields}, status = status.HTTP_400_BAD_REQUEST)

           

            # if customer is updating an appointment   
            service_type = ServiceType.objects.get(pk=request.data["service_type"])
            appointment.service_type = service_type
            progress = Progress.objects.get(pk=request.data["progress"])
            appointment.progress = progress
            appointment.request_date = request.data["request_date"]
            appointment.scheduled = request.data["scheduled"]
            appointment.image = request.data["image"]
            appointment.confirm = request.data["confirm"]
            appointment.consultation = request.data["consultation"]
            appointment.request_details = request.data["request_details"]

            appointment.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        try:
            appointment = Appointments.objects.get(pk=pk)
            appointment.delete()
            return Response({"message": "This appointment has been DELETED"}, status=status.HTTP_204_NO_CONTENT)
        except Appointments.DoesNotExist:
            return Response({"message": "The appointment you specified does not exist"}, status = status.HTTP_404_NOT_FOUND)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model =  User
        fields = ('id','is_staff', )

class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model = Customer
        fields = ('id', 'full_name', 'user', 'address',)

class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model = Employee
        fields = ('id', 'full_name', 'user', 'address',)

class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Progress
        fields = ('id','label', 'percent', 'class_name',)


class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = ('id', 'name','description',)

class AppointmentsSerializer(serializers.ModelSerializer):
    service_type = ServiceTypeSerializer(many=False)
    progress = ProgressSerializer(many=False)
    customer = CustomerSerializer(many=False)
    employee = EmployeeSerializer(many=True)
    class Meta:
        model = Appointments
        fields = ('id', 'service_type','completed', 'progress', 'consultation', 
                  'request_details', 'request_date', 'customer', 'employee', 'scheduled', 
                  'image', 'confirm', )
