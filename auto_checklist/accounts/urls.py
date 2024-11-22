from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    UserRegisterAPIView
)


urlpatterns = [
    path("register/", UserRegisterAPIView.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name="token"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh")

]