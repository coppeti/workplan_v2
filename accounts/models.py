from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(blank=True, unique=True, max_length=30)
    email = models.EmailField(unique=True)
    birthday = models.DateField()
    is_active = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        self.first_name = self.first_name.lower()
        self.last_name = self.last_name.lower()
        self.email = self.email.lower()

        super().save(*args, **kwargs)
