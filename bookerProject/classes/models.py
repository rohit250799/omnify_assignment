from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.name} - {self.email}'

class FitnessClass(models.Model):
    name = models.CharField(max_length=255)
    date_time = models.DateTimeField()
    instructor = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name} - {self.date_time}'
    
class AvailableSlot(models.Model):
    fitness_class = models.ForeignKey(FitnessClass, related_name='slots', on_delete=models.CASCADE)
    slot_time = models.DateTimeField()
    capacity = models.PositiveIntegerField(default=1) #represents how many users can book this 

    def __str__(self):
        return f'{self.fitness_class.name} - {self.slot_time}'

#The Booking model acts as a through model between User and FitnessClass, while also connecting with AvailableSlot to show which slots were booked    
class Bookings(models.Model):
    user = models.ForeignKey(User, related_name='bookings', on_delete=models.CASCADE)
    fitness_class = models.ForeignKey(FitnessClass, related_name='bookings', on_delete=models.CASCADE)
    slots_booked = models.ManyToManyField(AvailableSlot)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.user.name} booked {self.quantity} slots in {self.fitness_class.name}'
