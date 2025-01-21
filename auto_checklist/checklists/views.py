from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import (
    Element,
    Check,
    Category
)
from .serializers import (
    ElementSerializer,
    CheckSerializer,
    CategorySerializer
)


class ElementsListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Element.objects.all()
    serializer_class = ElementSerializer


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


