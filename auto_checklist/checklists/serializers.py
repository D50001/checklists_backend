from rest_framework.serializers import ModelSerializer, ReadOnlyField
from .models import Element, Check, Category


class ElementSerializer(ModelSerializer):
    class Meta:
        model = Element
        fields = "__all__"


class CheckSerializer(ModelSerializer):
    class Meta:
        model = Check
        fields = "__all__"


class CategorySerializer(ModelSerializer):
    readable_title = ReadOnlyField()
    class Meta:
        model = Category
        fields = ["id", "title", "readable_title"]