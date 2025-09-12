from django.urls import path

from .serializers import CategoryExtendedSerializer
from .views import (
    ElementsListAPIView,
    CheckCreateAPIView,
    CategoryListView,
    CheckMultipleCreateAPIView,
    SubCategoryListView,
    CategoryExtendedListAPIView,
    CommentAPIView
)


urlpatterns = [
    path("elements/", ElementsListAPIView.as_view(), name="elements-list"),
    path("checks/", CheckCreateAPIView.as_view(), name="check-create"),
    path("multicheks/", CheckMultipleCreateAPIView.as_view(), name="multiple-check"),
    path("categories/", CategoryListView.as_view(), name="categories-list"),
    path("subcategories/", SubCategoryListView.as_view(), name="subcategories-list"),
    path("categories_extended/", CategoryExtendedListAPIView.as_view(), name="categories-extended"),
    path("comment/", CommentAPIView.as_view(), name="comment"),
]