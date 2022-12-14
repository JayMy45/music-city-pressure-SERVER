import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from mcpressureapi.models import ServiceType, Equipment, Employee

class ServiceTests(APITestCase):
    fixtures = ['user', 'tokens', 'customer', 'employee',
                'equipment', 'service_type']

    def setUp(self):
        self.employee = Employee.objects.first()
        token = Token.objects.get(user=self.employee.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        

    def test_get_service(self):
        """
        Ensure we can get an existing service.
        """

        # Seed the database with a service
        service = ServiceType()
        service.name = "Side Walk Pressure Wash"
        service.label = "Pressure Wash"
        service.image = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSJNN_FhsZzL0m-FZq2Fu8PQunmaF_lKBJBDEpe2ihMlDQ60JyFD5Ns3ru3ThsXy7KWAdc&usqp=CAU"
        service.description = "Washing with pressure"
        service.details = "Pressure with washing"
        service.price = 250
        eq1 = Equipment.objects.get(pk=1)
        eq2 = Equipment.objects.get(pk=2)
        service.save()

        
        service.tools.set([eq1,eq2])
        # service.tools.add(equipment_id)


        # Initiate request and store response
        response = self.client.get(f"/services/{service.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["name"], "Side Walk Pressure Wash")
        self.assertEqual(json_response["image"], "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSJNN_FhsZzL0m-FZq2Fu8PQunmaF_lKBJBDEpe2ihMlDQ60JyFD5Ns3ru3ThsXy7KWAdc&usqp=CAU")
        self.assertEqual(json_response["label"], "Pressure Wash")
        self.assertEqual(json_response["description"], "Washing with pressure")
        self.assertEqual(json_response["details"], "Pressure with washing")
        self.assertEqual(json_response["price"], 250)
        self.assertEqual(json_response["tools"][0]["id"], 1)
        self.assertEqual(json_response["tools"][1]["id"], 2)
