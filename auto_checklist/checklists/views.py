from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Element, Check
from .serializers import ElementSerializer, CheckSerializer


class ElementsListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Element.objects.all()
    serializer_class = ElementSerializer


class CheckCreateAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Check.objects.all()
    serializer_class = CheckSerializer