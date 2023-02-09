from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

# from colorfield.fields import ColorField

from accounts.models import CustomUser


class Activities(models.Model):
    name = models.CharField(max_length=100, unique=True)
    short_name = models.CharField(max_length=3, unique=True)
    background_color = models.CharField(max_length=9, blank=True)
    text_color = models.CharField(max_length=9, blank=True)
    
    def save(self, *args, **kwargs):
        self.name = self.name.title()
        self.short_name = self.short_name.upper()
        super().save(*args, **kwargs)
    

class Events(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    activity_id = models.ForeignKey(Activities, on_delete=models.PROTECT)
    date_start = models.DateField()
    date_stop = models.DateField()
    confirmed = models.BooleanField(default=False)
    changed_on = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    displayed = models.BooleanField(default=False)
    comment = models.TextField(max_length=300, blank=True)
    
    def clean(self):
        if self.date_stop < self.date_start:
            raise ValidationError('Das Enddatum liegt vor dem Startdatum.')