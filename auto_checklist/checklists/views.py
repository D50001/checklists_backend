import logging
import os
import uuid

from django.core.files.base import ContentFile
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import (
    Element,
    Check,
    Category,
    SubCategory
)
from .serializers import (
    ElementSerializer,
    CheckSerializer,
    CategorySerializer,
    SubCategorySerializer,
    CategoryExtendedSerializer,
    CommentSerializer
)
from django.core.files.storage import default_storage

from .tasks import transcribe_call_and_add_comment


class ElementsListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Element.objects.all()
    serializer_class = ElementSerializer

    def get_queryset(self):
        category_id = self.request.query_params.get("category")
        subcategory_id = self.request.query_params.get("subcategory")
        queryset = super().get_queryset()

        if category_id:
            queryset = queryset.filter(category=category_id)
        if subcategory_id:
            queryset = queryset.filter(sub_category=subcategory_id)
        
        return queryset


class CheckCreateAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Check.objects.all()
    serializer_class = CheckSerializer


class CheckMultipleCreateAPIView(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        """
        Structure of request:
            [
                {
                "order": int,
                "element": int,
                "state": str
                },
                {
                "order": int,
                "element": int,
                "state": str,
                "photo": photo
                },
                ...
            ]
        """
        serializer = CheckSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubCategoryListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        category_id = self.request.query_params.get("category")
        if category_id:
            return super().get_queryset().filter(category=category_id)
        return super().get_queryset()


class CategoryExtendedListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Category.objects.all()
    serializer_class = CategoryExtendedSerializer


class CommentAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        logging.info(data)
        voice_message = data['voice_message']

        file_content = voice_message.read()
        file_extension = voice_message.name.split('.')[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"

        file_path = default_storage.save(
            f"files/{unique_filename}",
            ContentFile(file_content)
        )
        print(file_path)
        transcribe_call_and_add_comment.delay(data['order'], data['element'], file_path)

        return Response({"ok": True}, status=status.HTTP_200_OK)