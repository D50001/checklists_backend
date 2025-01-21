from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from ..models import Order, Department, Car
from rest_framework import status


User = get_user_model()


class ListOrdersAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email="test@test.com",
            username="test_user",
            password="test_password"
        )
        self.url = "/api/orders/"

        self.department = Department.objects.create(title="test_department", telegram_chat_id=111111111111)
        self.car = Car.objects.create(
            model="Toyota Camry",
            vin="ANY16SYMBOLSVIN",
        )
        self.order = Order.objects.create(
            number="A11101",
            date="2025-01-01",
            car=self.car,
            department=self.department
        )

    def test_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        response_count = response.data.get("count", 0)
        orders_count = Order.objects.all().count()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_count, orders_count)

    def test_error_unauthorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_error_invalid_method(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
