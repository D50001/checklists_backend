from django.db import models
from orders.models import Order


class Element(models.Model):

    element = models.CharField(
        max_length=32, # max lenght to process to telegram callback query
        unique=True
        )

    def __str__(self):
        return self.element

    class Meta:
        verbose_name = "Элемент"
        verbose_name_plural = "Элементы"


class Check(models.Model):
    STATES = (
        ("OK", "Ремонт не требуется"),
        ("NOT_OK", "Требуется ремонт")
    )
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    element = models.ForeignKey(Element, on_delete=models.CASCADE)
    state = models.CharField(choices=STATES, default="OK", verbose_name="Состояние")

    def __str__(self):
        return self.element.element