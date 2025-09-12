from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from ..models import Order, Department, Car
from rest_framework import status
from checklists.models import (
    Element,
    Category,
    SubCategory,
    Check
)

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
        self.category = Category.objects.create(title="Тормозная система")
        self.subcategory = SubCategory.objects.create(
            category=self.category,
            title="Передние тормозные колодки"
        )
        self.element = Element.objects.create(
            element="Передние тормозные колодки левые",
            category=self.category,
            sub_category=self.subcategory
            )

    def test_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        response_count = response.data.get("count", 0)
        orders_count = Order.objects.all().count()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_count, orders_count)
        order_data = response.data.get("results", [])[0]
        self.assertEqual(order_data.get("checks"), [])
        self.assertEqual(order_data.get("is_closed"), False)

    def test_success_no_closed_orders(self):
        self.client.force_authenticate(user=self.user)
        check = Check.objects.create(
            order=self.order,
            element=self.element
        )
        response = self.client.get(self.url)
        response_count = response.data.get("count", 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_count, 0)

    def test_error_unauthorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_error_invalid_method(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class OrdersAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email="test@test.com",
            username="test_user",
            password="test_password"
        )

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
        self.category = Category.objects.create(title="Тормозная система")
        self.subcategory = SubCategory.objects.create(
            category=self.category,
            title="Передние тормозные колодки"
        )
        self.element = Element.objects.create(
            element="Передние тормозные колодки левые",
            category=self.category,
            sub_category=self.subcategory
            )
        self.url = f"/api/order/{self.order.id}/"

    def test_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        is_closed = response.data.get("is_closed")
        checks = response.data.get("checks")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(is_closed, False)
        self.assertEqual(checks, [])

    def test_success_close_order(self):
        self.client.force_authenticate(user=self.user)
        check = Check.objects.create(
            order=self.order,
            element=self.element
        )
        response = self.client.get(self.url)
        is_closed = response.data.get("is_closed")
        checks = response.data.get("checks")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(is_closed, True)
        self.assertEqual(len(checks), 1)

    def test_success_multiple_checks(self):
        self.client.force_authenticate(user=self.user)
        element = Element.objects.create(
            element="Передние колодки правые",
            category=self.category,
            sub_category=self.subcategory
            )
        check = Check.objects.create(
            order=self.order,
            element=self.element
        )
        response = self.client.get(self.url)
        is_closed = response.data.get("is_closed")
        checks = response.data.get("checks")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(is_closed, False)
        self.assertEqual(len(checks), 1)