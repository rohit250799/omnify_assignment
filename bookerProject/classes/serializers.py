from rest_framework import serializers
from .models import Bookings

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookings
        fields = ['id', 'user', 'bookedWithMail', 'fitness_class', 'slots_booked', 'quantity', 'createdAt']
        read_only_fields = ['bookedWithMail', 'createdAt']