from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import ModelSerializer
from .models import UserProfile


class RegistrationSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["id", "username", "password", "email"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        validate_password(data["password"])
        return data

    def create(self, validated_date):
        password = validated_date.pop("password")
        queryset = UserProfile.objects.create(**validated_date)
        queryset.set_password(raw_password=password)
        queryset.save()
        return queryset