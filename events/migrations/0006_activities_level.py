# Generated by Django 4.1.7 on 2023-03-11 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_alter_events_date_start_alter_events_date_stop'),
    ]

    operations = [
        migrations.AddField(
            model_name='activities',
            name='level',
            field=models.CharField(choices=[(2, 'Techniker'), (4, 'Manager'), (6, 'Admin'), (8, 'Superuser')], default=2, max_length=1),
        ),
    ]
