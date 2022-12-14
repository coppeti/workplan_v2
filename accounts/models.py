from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    username = models.CharField(blank=True, unique=True, max_length=30)
    email = models.EmailField(unique=True, blank=False)
    birthday = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    email_confirmed = models.BooleanField(default=False)
    reset_password = models.BooleanField(default=False)
    
    # TODO: check if username is unique
    def save(self, *args, **kwargs):
        self.first_name = self.first_name.lower()
        self.last_name = self.last_name.lower()
        self.username = self.username.lower()
        self.email = self.email.lower()

        super().save(*args, **kwargs)
