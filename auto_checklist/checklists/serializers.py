from rest_framework.serializers import ModelSerializer
from .models import Element, Check


class ElementSerializer(ModelSerializer):
    class Meta:
        model = Element
        fields = "__all__"


class CheckSerializer(ModelSerializer):
    class Meta:
        model = Check
        fields = "__all__"