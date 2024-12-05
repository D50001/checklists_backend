from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from ..models import Element, Category


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



    