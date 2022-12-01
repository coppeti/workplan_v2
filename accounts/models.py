from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


LOW_LETTER_REGEX = RegexValidator(r'^[a-z]{3,}$')


class UserManager(BaseUserManager):
    def _create_user(self, email, password, is_active, is_staff, is_superuser, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, is_active=is_active, is_staff=is_staff, is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, False, False, False, **extra_fields)
    
    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, True, **extra_fields)
    


class User(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True, validators=[LOW_LETTER_REGEX])
    email = models.EmailField(unique=True)
    birthday = models.DateField(null=True)
    is_active = models.BooleanField(default=False)
    
    objects = UserManager()
    
    def __str__(self):
        return f'{self.first_name.title()} {self.last_name.upper()}'
    
    def save(self, *args, **kwargs):
        self.first_name = self.first_name.lower()
        self.last_name = self.last_name.lower()
        
        super().save(*args, **kwargs)
