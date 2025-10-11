from django.db import models
from django.contrib.auth.models import AbstractUser
class User(AbstractUser):
    contactNo = models.CharField(max_length=15)
    address = models.TextField()
    is_provider = models.BooleanField(default=False)

    class Meta:
        db_table = 'users_user'

    def __str__(self):
        return self.username
