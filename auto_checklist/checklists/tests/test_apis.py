from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from ..models import Element, Category
from orders.models import Department, Car, Order
from PIL import Image
from uuid import UUID
from django.core.files.base import ContentFile
from io import BytesIO


User = get_user_model()


class ElementsListAPIViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="test@test.com",
            username="test_user",
            password="test_password"
        )
        self.element = Element.objects.create(element="Передние тормозные колодки")
        self.url = "/api/elements/"
        self.client = APIClient()

    def create_element(self):
        Element.objects.create(element="Задние тормозные колодки")

    def test_success_one_item(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        elements_count = Element.objects.all().count()
        self.assertEqual(len(response.data), elements_count)

    def test_success_two_items(self):
        self.create_element()
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        elements_count = Element.objects.all().count()
        self.assertEqual(len(response.data), elements_count)

    def test_error_unauthorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_error_invalid_payload(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class CheckCreateTest(APITestCase):
    
    def setUp(self):
        self.department = Department.objects.create(title="test_dapertment", telegram_chat_id=111111111111)
        self.car = Car.objects.create(
            model="Toyota Camry",
            vin="ANY16SYMBOLSVIN",
        )
        self.order = Order.objects.create(
            number="A11101",
            date="2024-01-01",
            car=self.car,
            department=self.department
        )
        self.user = User.objects.create(
            email="test@test.com",
            username="test_user",
            password="test_password"
        )
        self.element = Element.objects.create(element="Передние тормозные колодки")
        self.url = "/api/checks/"

    def create_image(self, width=1, height=1):
        image = Image.new('RGB', (width, height), color='white')
        byte_io = BytesIO()
        image.save(byte_io, format='PNG')
        byte_io.seek(0)
        return ContentFile(byte_io.read(), name='test_image.png')

    def test_success_required_fields(self):
        self.client.force_authenticate(user=self.user)
        payload = {
            "order": self.order.id,
            "element": self.element.id,
            "state": "OK"
        }
        response = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("order"), self.order.id)

    def test_success_all_fields(self):
        image = self.create_image()
        self.client.force_authenticate(user=self.user)
        payload = {
            "order": self.order.id,
            "element": self.element.id,
            "state": "OK",
            "photo": image
        }
        response = self.client.post(self.url, data=payload, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("order"), self.order.id)

    def test_error_unauthorized(self):
        payload = {
            "order": self.order.id,
            "element": self.element.id,
            "state": "OK"
        }
        response = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_error_invalid_payload(self):
        self.client.force_authenticate(user=self.user)
        payload = {
            "order": self.order.id,
            "state": "NOT_OK"
        }
        response = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_error_invalid_method(self):
        self.client.force_authenticate(user=self.user)
        payload = {
            "order": self.order.id,
            "element": self.element.id,
            "state": "OK"
        }
        response = self.client.patch(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class CategoryListViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email="test@test.com",
            username="test_user",
            password="test_password"
        )
        self.category = Category.objects.create(title="BRAKES")
        self.url = "/api/categories/"

    def test_retrieve_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(len(response.data), Category.objects.all().count())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0].get("id"), self.category.id)

    def test_error_unauthorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_error_invalid_method(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)



    