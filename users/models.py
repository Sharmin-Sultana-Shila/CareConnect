from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """User model for customers/clients"""
    contactNo = models.CharField(max_length=15)
    address = models.TextField()
    profile_image = models.ImageField(upload_to='user_profiles/', blank=True, null=True)
    is_provider = models.BooleanField(default=False)

    def __str__(self):
        return self.username