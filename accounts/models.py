from datetime import timezone
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


# class CustomUserManager(BaseUserManager):
#     def _create_user(self, email, password, is_active, is_staff, is_superuser, **extra_fields):
#         now = timezone.now()
#         if not email:
#             raise ValueError('Die E-Mail muss eingestellt werden')
#         email = self.normalize_email(email)
#         user = self.model(email=email, is_active=is_active, is_staff=is_staff, is_superuser=is_superuser, date_joined=now, **extra_fields)
#         user.set_password(password)
#         user.save()
#         return user
    
#     def create_user(self, email, password=None, **extra_fields):
#         return self._create_user(email, password, False, True, False, **extra_fields)
    
#     def create_superuser(self, email, password, **extra_fields):
#         return self._create_user(email, password, True, True, True, **extra_fields)
    

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    username = models.CharField(blank=True, unique=True, max_length=30)
    email = models.EmailField(unique=True, blank=False)
    birthday = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    
    # objects = CustomUserManager
    
    # TODO: check if username is unique
    def save(self, *args, **kwargs):
        self.first_name = self.first_name.lower()
        self.last_name = self.last_name.lower()
        self.username = f'{self.first_name[:2]}{self.last_name[:2]}'
        self.email = self.email.lower()

        super().save(*args, **kwargs)
