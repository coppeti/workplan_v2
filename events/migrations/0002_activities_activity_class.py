# Generated by Django 4.1.6 on 2023-02-10 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='activities',
            name='activity_class',
            field=models.CharField(default='a', max_length=100, unique=True),
            preserve_default=False,
        ),
    ]
