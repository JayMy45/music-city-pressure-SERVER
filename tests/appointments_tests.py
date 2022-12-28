# import json
# from rest_framework import status
# from rest_framework.test import APITestCase
# from mcpressureapi.models import Appointments
# from mcpressureapi.models import Customer
# from rest_framework.authtoken.models import Token


# class AppointmentTests(APITestCase):

#     # Add fixtures need to run to build the test database
#     fixtures = ['user','tokens','customer','employee',
#                 'location','progress','equipment','service_type',
#                 'appointments',]

#     def setUp(self):
#         self.customer = Customer.objects.first()
#         token = Token.objects.get(user=self.customer.user)
#         self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

#     def test_create_appointment(self):
#         """
#         Ensure a new appointment can be created.
#         """

#         # Define the endpoint in the API where the request will be sent
#         url = "/appointments"

#         # Define the request body
#         data = {
#             "employee": 1,
#             "customer": 1,
#             "service_type": 1,
#             "request_date": "2023-03-23",
#             "scheduled": False,
#             "date_completed": "2022-11-07",
#             "progress": 1,
#             "consultation": False,
#             "completed": False,
#             "confirm": False,
#             "request_details": "Need this roof done like yesterday",
#         }

#         # Initiate request and store response
#         response = self.client.post(url, data, format='json')

#         # Parse the JSON in teh response body
#         json_response = json.loads(response.content)

#         # Assert that the game was created
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#         # Assert that the properties on the created resource are correct
#         self.assertEqual(json_response["employee"], 1)
#         self.assertEqual(json_response["customer"], 1)
#         self.assertEqual(json_response["service_type"], 1)
#         self.assertEqual(json_response["request_date"], "2023-03-23")
#         self.assertEqual(json_response["scheduled"], False)
#         self.assertEqual(json_response["date_completed"], "2022-11-07")
#         self.assertEqual(json_response["progress"], 1)
#         self.assertEqual(json_response["consultation"], False)
#         self.assertEqual(json_response["completed"], False)
#         self.assertEqual(json_response["confirm"], False)
#         self.assertEqual(json_response["request_details"], "Need this roof done like yesterday")