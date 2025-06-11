from rest_framework import serializers
from .models import Bookings, FitnessClass, AvailableSlot

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookings
        fields = ['id', 'user', 'bookedWithMail', 'fitness_class', 'slots_booked', 'quantity', 'createdAt']
        read_only_fields = ['bookedWithMail', 'createdAt']

class FitnessClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessClass
        fields = ['id', 'name', 'date_time', 'instructor']

class AvailableSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableSlot
        fields = ['id', 'slot_time', 'capacity']