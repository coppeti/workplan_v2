# Generated by Django 4.1.7 on 2023-04-28 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_customuser_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.IntegerField(choices=[(2, 'Techniker'), (4, 'Manager'), (6, 'Supervisor'), (8, 'Superuser')], default=2, verbose_name='Rolle'),
        ),
    ]