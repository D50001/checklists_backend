from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import (
    Serializer,
    ModelSerializer,
    CharField,
    DateField,
    IntegerField,
)
from .models import Car, Order, Department
from telegram.notificator import TelegramNotificator

from checklists.serializers import CheckSerializer
from checklists.models import Element


class CarOrderSerializer(Serializer):
    """Serializer for both car and order endpoint"""
    number = CharField(max_length=20)
    date = DateField()
    model = CharField(max_length=100)
    year = IntegerField(required=False)
    vin = CharField(max_length=100)
    mileage = IntegerField(required=False)
    license_number = CharField(required=False)
    department = CharField(max_length=20)

    def validate(self, attrs):
        number = attrs.get("number")
        date = attrs.get("date")
        model = attrs.get("model")
        year = attrs.get("year")
        vin = attrs.get("vin")
        mileage = attrs.get("mileage")
        license_number = attrs.get("license_number")
        department = attrs.get("department")
        try:
            department = Department.objects.get(title=department)
        except Department.DoesNotExist:
            raise ValidationError("No department found")
        car, _ = Car.objects.update_or_create(
            vin=vin,
            defaults={
                "model": model,
                "year": year,
                "mileage": mileage,
                "license_number": license_number
            })
        orders = Order.objects.filter(number=number, date=date)
        if not orders.exists():
            order = Order.objects.create(
                    number=number,
                    date=date,
                    car=car,
                    department=department
                )
            order_id = order.id
        else:
            order_id = orders.first().id
        telegram_api = TelegramNotificator()
        telegram_api.send_order_notification(attrs, order_id)
        return attrs
    

class CarSerializer(ModelSerializer):
    class Meta:
        model = Car
        fields = "__all__"


class OrderSerializer(ModelSerializer):
    car = CarSerializer()
    checks = CheckSerializer(many=True)
    is_closed = SerializerMethodField()
    
    class Meta:
        model = Order
        fields = "__all__"

    def get_is_closed(self, obj):
        obj_checks = obj.checks.values_list("element__id", flat=True).distinct().count()
        elements_ids = Element.objects.all().values_list("id", flat=True).distinct().count()
        #TODO: сделать проверку более надежной
        return obj_checks == elements_ids


