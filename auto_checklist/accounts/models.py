from django.contrib.auth.models import AbstractUser
from django.db import models


class UserProfile(AbstractUser):
    email = models.EmailField(verbose_name="Email", unique=True)
