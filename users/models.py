from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    year = models.CharField(max_length=10)
    department = models.CharField(max_length=50)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username
