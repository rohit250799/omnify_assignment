import pytest
from rest_framework.test import APIClient
from classes.models import FitnessClass, AvailableSlot, Bookings
from django.utils import timezone

@pytest.mark.django_db
def test_successful_booking():
    client = APIClient()

    fitness_class = FitnessClass.objects.create(
        name="Zumba",
        date_time=timezone.now() + timezone.timedelta(days=2),
        instructor="John Smith"
    )

    slot = AvailableSlot.objects.create(
        fitness_class=fitness_class,
        slot_time=fitness_class.date_time,
        capacity=5
    )

    payload = {
        "class_id": fitness_class.id,
        "client_name": "Rohit",
        "client_email": "rohit@example.com",
        "slot_ids": [slot.id],
        "quantity": 2
    }

    response = client.post('/book/', payload, format='json')

    assert response.status_code == 201
    assert Bookings.objects.count() == 1

    booking = Bookings.objects.first()
    assert booking.bookedWithMail == "rohit@example.com"
    assert booking.slots_booked.first().id == slot.id
    assert booking.quantity == 2

@pytest.mark.django_db
def test_booking_slot_over_capacity():
    client = APIClient()

    fitness_class = FitnessClass.objects.create(
        name="HIIT",
        date_time=timezone.now() + timezone.timedelta(days=2),
        instructor="Mike"
    )

    slot = AvailableSlot.objects.create(
        fitness_class=fitness_class,
        slot_time=fitness_class.date_time,
        capacity=1
    )

    payload = {
        "class_id": fitness_class.id,
        "client_name": "Alex",
        "client_email": "alex@example.com",
        "slot_ids": [slot.id],
        "quantity": 2  # exceeds capacity
    }

    response = client.post('/book/', payload, format='json')
    assert response.status_code == 400
    assert "overbooked" in response.json()['error'].lower()
