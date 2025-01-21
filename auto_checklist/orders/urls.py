from django.urls import path
from .views import (
    CreateCarOrderAPIView,
    ListOrdersAPIView
)


urlpatterns = [
    path("checklist_order_car/", CreateCarOrderAPIView.as_view(), name="create_car_order"),
    path("orders/", ListOrdersAPIView.as_view(), name="orders")
]