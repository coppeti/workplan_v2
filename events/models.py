from django.core.exceptions import ValidationError
from django.db import models

from accounts.models import CustomUser


class Activities(models.Model):
    name = models.CharField(max_length=100, unique=True)
    short_name = models.CharField(max_length=3, unique=True)
    

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