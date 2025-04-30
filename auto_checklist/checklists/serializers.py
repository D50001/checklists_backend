from rest_framework.serializers import ModelSerializer, ReadOnlyField
from .models import (
    Element,
    Check,
    Category,
    Recommendation,
    SubCategory
)


class ElementSerializer(ModelSerializer):
    class Meta:
        model = Element
        fields = "__all__"


class CheckSerializer(ModelSerializer):
    class Meta:
        model = Check
        fields = "__all__"

    def create(self, validated_data):
        superb = super().create(validated_data)

        state = validated_data.get("state")
        order = validated_data.get("order")
        element = validated_data.get("element")

        if state == "NOT_OK":
            Recommendation.objects.create(
                car=order.car,
                element=element,
            )
        return superb


class CategorySerializer(ModelSerializer):
    readable_title = ReadOnlyField()

    class Meta:
        model = Category
        fields = ["id", "title", "readable_title"]


class SubCategorySerializer(ModelSerializer):
    class Meta:
        model = SubCategory
        fields = "__all__"