# Generated by Django 4.1.6 on 2023-02-09 21:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('short_name', models.CharField(max_length=3, unique=True)),
                ('background_color', models.CharField(blank=True, max_length=9)),
                ('text_color', models.CharField(blank=True, max_length=9)),
            ],
        ),
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_start', models.DateField()),
                ('date_stop', models.DateField()),
                ('confirmed', models.BooleanField(default=False)),
                ('changed_on', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('displayed', models.BooleanField(default=False)),
                ('comment', models.TextField(blank=True, max_length=300)),
                ('activity_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='events.activities')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
