# Generated by Django 4.1.6 on 2023-02-14 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_activities_activity_class'),
    ]

    operations = [
        migrations.AddField(
            model_name='activities',
            name='displayed',
            field=models.BooleanField(default=True),
        ),
    ]