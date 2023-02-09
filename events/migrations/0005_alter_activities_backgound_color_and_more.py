# Generated by Django 4.1.6 on 2023-02-08 21:15

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_alter_activities_backgound_color_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activities',
            name='backgound_color',
            field=colorfield.fields.ColorField(default='#FF0000', image_field=None, max_length=18, samples=None),
        ),
        migrations.AlterField(
            model_name='activities',
            name='text_color',
            field=colorfield.fields.ColorField(default='#000000', image_field=None, max_length=18, samples=None),
        ),
    ]
