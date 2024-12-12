from django.db import models
from orders.models import Order, Car
from django.utils.html import format_html


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
        ("NOT_OK", "Несправно"),
    )
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    element = models.ForeignKey(Element, on_delete=models.CASCADE)
    state = models.CharField(choices=STATES, default="OK", verbose_name="Состояние")
    photo = models.ImageField(null=True, blank=True, verbose_name="Фото", upload_to="media/images/")

    def image_tag(self):
        if self.photo:
            return format_html('<img src="{}" style="width: 100px; height: auto;" />', self.photo.url)
        return ""

    def __str__(self):
        return self.element.element


class Recommendation(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    element = models.ForeignKey(Element, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.element}: обнаружена неисправность."