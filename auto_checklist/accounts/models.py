from django.contrib.auth.models import AbstractUser
from django.db import models
from orders.models import Department


class UserProfile(AbstractUser):
    email = models.EmailField(verbose_name="Email", unique=True)
    department = models.ForeignKey(Department, related_name="users", on_delete=models.SET_NULL, null=True)
