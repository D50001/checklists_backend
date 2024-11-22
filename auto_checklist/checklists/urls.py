from django.urls import path
from .views import ElementsListAPIView, CheckCreateAPIView


urlpatterns = [
    path("elements/", ElementsListAPIView.as_view(), name="elements-list"),
    path("checks/", CheckCreateAPIView.as_view(), name="check-create")
]