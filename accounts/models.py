from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    TECHNICIAN = 2
    MANAGER = 4
    ADMIN = 6
    SUPERUSER = 8
    USER_ROLE = [
        (TECHNICIAN, 'Techniker'),
        (MANAGER, 'Manager'),
        (ADMIN, 'Admin'),
        (SUPERUSER, 'Superuser'),
    ]

    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    username = models.CharField(blank=True, unique=True, max_length=30, verbose_name='Pseudo')
    email = models.EmailField(unique=True, blank=False)
    birthday = models.DateField(blank=True, null=True)
    role = models.IntegerField(choices=USER_ROLE, default=2, verbose_name='Rolle')
    is_active = models.BooleanField(default=False)
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.first_name.title()} {self.last_name.upper()}'

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.lower()
        self.last_name = self.last_name.lower()
        self.username = self.username.lower()
        self.email = self.email.lower()

        super().save(*args, **kwargs)
