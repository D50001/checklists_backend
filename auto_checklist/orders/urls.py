from django.urls import path
from .views import (
    CreateCarOrderAPIView,
)


urlpatterns = [
    path("order_car/", CreateCarOrderAPIView.as_view(), name="create_car_order"),
]