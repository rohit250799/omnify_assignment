# Generated by Django 5.2.2 on 2025-06-09 11:49

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookings',
            name='bookedWithMail',
            field=models.EmailField(default='placeholder@example.com', max_length=254),
        ),
        migrations.AddField(
            model_name='bookings',
            name='createdAt',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
