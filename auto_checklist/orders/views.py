import datetime
import logging

from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, ListAPIView
import json
from .serializers import (
    CarOrderSerializer,
    OrderSerializer
)
from .models import Order
from .paginations import OrderPagination
from .services import get_filtered_orders

logger = logging.getLogger(__name__)


class CreateCarOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer = CarOrderSerializer

    def post(self, request):
        """
        Structure of request:
            {
                "number": "Y-0028",
                "date": "2024-01-01",
                "model": "Toyota RAV4",
                "year": 2023,
                "vin": "ANY16SYMBOLSVIN",
                "mileage": 50000,
                "license_number": "A444XX777",
                "department": "Полтавская"
            }
        """
        data = request.body.decode('utf-8-sig')
        try:
            data = json.loads(data)
        except json.JSONDecodeError as e:
            logger.debug(f"JSON Decode Error: {str(e)}")
            data = json.loads(request.body)

        logger.info(data)

        serializer = self.serializer(data=data)

        if serializer.is_valid(raise_exception=True):
            return Response({"ok": True}, status=status.HTTP_201_CREATED)


class ListOrdersAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    pagination_class = OrderPagination

    def get_queryset(self):
        return get_filtered_orders()


class OrderDetailAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()