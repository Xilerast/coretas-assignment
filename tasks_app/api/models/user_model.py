from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """User model for task api"""
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self) -> str:
        return "Username: " + self.username + "\nE-Mail: " + self.email