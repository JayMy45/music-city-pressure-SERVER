from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import force_authenticate
from mcpressureapi.models import Customer, ServiceType, Progress, Appointments, EmployeeAppointment, Employee

class CreateAppointmentTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Create user objects
        self.staff_user = User.objects.create_user(username='staff_user', password='password')
        self.staff_user.is_staff = True
        self.staff_user.save()

        self.customer_user = User.objects.create_user(username='customer_user', password='password')

        # Create token for staff user
        self.staff_token = Token.objects.create(user=self.staff_user)

        # Create token for customer user
        self.customer_token = Token.objects.create(user=self.customer_user)

        # Create customer object
        self.customer = Customer.objects.create(user=self.customer_user)

        # Create service type object
        self.service_type = ServiceType.objects.create(name='Test Service Type')

        # Create progress object
        self.progress = Progress.objects.create(name='Test Progress')

        # Create employee objects
        self.employee1 = User.objects.create_user(username='employee1', password='password')
        self.employee2 = User.objects.create_user(username='employee2', password='password')

        # Create employee objects
        self.employee1_obj = Employee.objects.create(user=self.employee1)
        self.employee2_obj = Employee.objects.create(user=self.employee2)

    def test_create_appointment_by_staff(self):
        # Staff user creates appointment
        data = {
            'service_type': self.service_type.id,
            'request_date': '2022-05-05',
            'request_details': 'Test request details',
            'image': 'Test image',
            'progress': self.progress.id,
            'employee': [self.employee1_obj.id, self.employee2_obj.id],
            'completed': False,
        }
        response = self.client.post(
            '/api/appointments/',
            data,
            HTTP_AUTHORIZATION=f'Token {self.staff_token.key}'
        )

        # Check status code is 201
        self.assertEqual(response.status_code, 201)

        # Check appointment is created with the given data
        appointment = Appointments.objects.get(id=response.data['id'])
        self.assertEqual(appointment.customer, self.customer)
        self.assertEqual(appointment.service_type, self.service_type)
        self.assertEqual(appointment.request_details, 'Test request details')
        self.assertEqual(appointment.image, 'Test image')
        self.assertEqual(appointment.progress, self.progress)
        self.assertEqual(appointment.completed, False)
        # Check that the employee appointments have been created
        employee_appointments = EmployeeAppointment.objects.filter(appointment=appointment)
        self.assertEqual(employee_appointments.count(), 2)
        self.assertIn(employee_appointments[0].employee, [self.employee1_obj, self.employee2_obj])
        self.assertIn(employee_appointments[1].employee, [self.employee1_obj, self.employee2_obj])


    def test_create_appointment_by_customer(self):
        # Customer user creates appointment
        data = {
            'service_type': self.service_type.id,
            'request_date': '2022-05-05',
            'request_details': 'Test request details',
            'image': 'Test image',
            'progress': self.progress.id,
            'employee': [self.employee1_obj.id, self.employee2_obj.id],
            'completed': False,
        }
        response = self.client.post(
            '/api/appointments/',
            data,
            HTTP_AUTHORIZATION=f'Token {self.customer_token.key}'
        )

        # Check status code is 201
        self.assertEqual(response.status_code, 201)

        # Check appointment is created with the given data
        appointment = Appointments.objects.get(id=response.data['id'])
        self.assertEqual(appointment.customer, self.customer)
        self.assertEqual(appointment.service_type, self.service_type)
        self.assertEqual(appointment.request_details, 'Test request details')
        self.assertEqual(appointment.image, 'Test image')
        self.assertEqual(appointment.progress, self.progress)
        self.assertEqual(appointment.completed, False)
        
        # Check that the employee appointments have been created
        employee_appointments = EmployeeAppointment.objects.filter(appointment=appointment)
        self.assertEqual(employee_appointments.count(), 2)
        self.assertIn(employee_appointments[0].employee, [self.employee1_obj, self.employee2_obj])
        self.assertIn(employee_appointments[1].employee, [self.employee1_obj, self.employee2_obj])


    def test_create_appointment(self):
    # create user and customer objects
        user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@example.com'
        )
        customer = Customer.objects.create(
            user=user,
            name='Test Customer'
        )
        
        # create a service type and progress object
        service_type = ServiceType.objects.create(
            name='Test Service Type'
        )
        progress = Progress.objects.create(
            name='Test Progress'
        )
        
        # create a request data object for appointment creation
        request_data = {
            'service_type': service_type.id,
            'request_date': '2023-01-01',
            'request_details': 'Test Request Details',
            'image': None,
            'progress': progress.id,
            'customer': customer.id,
        }
        
        # create a request object for appointment creation
        request = self.factory.post('/appointments/', data=request_data, format='json')
        force_authenticate(request, user=user)
        
        # call the create function and check if the response is 201
        response = self.create(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # check if the appointment object is created and contains correct data
        appointment = Appointments.objects.get(id=response.data['id'])
        self.assertEqual(appointment.service_type.id, service_type.id)
        self.assertEqual(appointment.request_date, '2023-01-01')
        self.assertEqual(appointment.request_details, 'Test Request Details')
        self.assertEqual(appointment.image, None)
        self.assertEqual(appointment.progress.id, progress.id)
        self.assertEqual(appointment.customer.id, customer.id)

