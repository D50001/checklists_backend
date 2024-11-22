from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


User = get_user_model()


class RegistrationViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            username="test_user",
            email="test@test.com",
            password="test_password"
        )
        self.url = "/api/accounts/register/"

    def test_success(self):
        payload = {
            "username": "user",
            "password": "123@testpassword@321",
            "email": "user@gmail.com"
        }
        response = self.client.post(self.url, data=payload, format="json")
        user_id = response.data.get("id")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 2)
        self.assertNotEqual(User.objects.get(id=user_id).password, "123@testpassword@321")


    def test_error_username_exists(self):
        payload = {
            "username": "test_user",
            "password": "123@testpassword@321",
            "email": "user@gmail.com"
        }
        response = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)