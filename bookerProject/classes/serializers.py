from rest_framework import serializers
from .models import Bookings, FitnessClass, AvailableSlot

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookings
        fields = ['id', 'user', 'bookedWithMail', 'fitness_class', 'slots_booked', 'quantity', 'createdAt']
        read_only_fields = ['bookedWithMail', 'createdAt']

class FitnessClassSerializer(serializers.ModelSerializer):
    available_slots = serializers.SerializerMethodField()
    class Meta:
        model = FitnessClass
        fields = ['id', 'name', 'date_time', 'instructor', 'available_slots']

    def get_available_slots(self, obj):
        slots = AvailableSlot.objects.filter(fitness_class=obj)
        return [
            {
                "id": slot.id,
                "slot_time": slot.slot_time,
                "capacity": slot.capacity    
            }
            for slot in slots
        ]

class AvailableSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableSlot
        fields = ['id', 'slot_time', 'capacity']