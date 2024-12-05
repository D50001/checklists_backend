from django.db import models
from orders.models import Order


class Category(models.Model):
    CATEGORIES = (
        ("ENGINE", "ДВС"),
        ("LIGHTING", "Свет"),
        ("SUSPENSION", "Подвеска"),
        ("BRAKES", "Тормоза"),
        ("EXHAUST", "Выхлоп")
    )

    title = models.CharField(choices=CATEGORIES)

    @property
    def readable_title(self) -> str:
        return dict(self.CATEGORIES).get(self.title, self.title)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Element(models.Model):

    element = models.CharField(
        max_length=32, # max length to process to telegram callback query
        unique=True
        )
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="elements"
    )

    def __str__(self):
        return self.element

    class Meta:
        verbose_name = "Элемент"
        verbose_name_plural = "Элементы"


class Check(models.Model):
    STATES = (
        ("OK", "Исправно"),
        ("NOT_OK", "Несправно, некритическое состояние"),
        ("CRITICAL", "Неисправно, критическое состояние"),
        ("ABSENCE", "Отсутствует")
    )
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    element = models.ForeignKey(Element, on_delete=models.CASCADE)
    state = models.CharField(choices=STATES, default="OK", verbose_name="Состояние")

    def __str__(self):
        return self.element.element