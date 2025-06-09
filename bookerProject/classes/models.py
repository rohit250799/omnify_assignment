from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User:
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.name} - {self.email}'

class FitnessClass:
    name = models.CharField(max_length=255)
    date_time = models.DateTimeField()
    instructor = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name} - {self.date_time}'
    