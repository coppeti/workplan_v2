# Generated by Django 4.1.6 on 2023-02-08 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_remove_customuser_reset_password_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(blank=True, max_length=30, unique=True, verbose_name='Pseudo'),
        ),
    ]