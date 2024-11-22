import uuid

from django.db import models


class Car(models.Model):
    model = models.CharField(max_length=100)
    year = models.IntegerField(null=True, blank=True)
    vin = models.CharField(max_length=100, unique=True)
    mileage = models.IntegerField(null=True, blank=True)
    license_number = models.CharField(max_length=100, null=True, blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.model} {self.license_number}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"


class Department(models.Model):

    telegram_chat_id = models.BigIntegerField()
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]
        verbose_name = "Филиал"
        verbose_name_plural = "Филиалы"


class Order(models.Model):
    number = models.CharField(max_length=20, verbose_name="Код")
    date = models.DateField(verbose_name="Дата")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    car = models.ForeignKey(Car, on_delete=models.PROTECT, related_name="orders", verbose_name="Автомобиль")
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="orders", verbose_name="Филиал")

    def __str__(self):
        return f"{self.number} {self.date}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Заказ-наряд"
        verbose_name_plural = "Заказ-наряды"
