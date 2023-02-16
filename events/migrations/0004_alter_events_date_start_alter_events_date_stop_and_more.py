# Generated by Django 4.1.6 on 2023-02-16 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_activities_displayed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='date_start',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='events',
            name='date_stop',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='events',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
