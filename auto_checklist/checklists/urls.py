from django.urls import path
from .views import (
    ElementsListAPIView,
    CheckCreateAPIView,
    CategoryListView,
    CheckMultipleCreateAPIView
)


urlpatterns = [
    path("elements/", ElementsListAPIView.as_view(), name="elements-list"),
    path("checks/", CheckCreateAPIView.as_view(), name="check-create"),
    path("multicheks/", CheckMultipleCreateAPIView.as_view(), name="multiple-check"),
    path("categories/", CategoryListView.as_view(), name="categories-list")
]