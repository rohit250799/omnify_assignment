import pytest
from rest_framework.test import APIClient
from classes.models import FitnessClass, AvailableSlot, Bookings, User
from django.utils import timezone

@pytest.mark.django_db
def test_booking_creation(user, fitness_class, available_slot):
    booking = Bookings.objects.create(
        user=user,
        bookedWithMail=user.email,
        fitness_class=fitness_class,
        quantity=2,
    )
    booking.slots_booked.add(available_slot)
    
    assert booking.slots_booked.count() == 1
    assert booking.user.name == "testuser"

@pytest.mark.django_db
def test_successful_booking():
    client = APIClient()

    user = User.objects.create(
        name="Test User",
        email="test@example.com",
        password="securepassword"
    )

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
        "slot_ids": [slot.id],
        "quantity": 2
    }

    response = client.post(f'http://127.0.0.1:8000/book-class/{user.id}/{fitness_class.id}/', payload, format='json')

    assert response.status_code == 201
    response_data = response.json()
    assert Bookings.objects.count() == 1

    assert response_data["user"] == user.id
    assert response_data["fitness_class"] == fitness_class.id
    assert response_data["quantity"] == 2
    assert set(response_data["slots_booked"]) == {slot.id}


@pytest.mark.django_db
def test_booking_slot_over_capacity():
    client = APIClient()

    user = User.objects.create(
        name="Test User",
        email="test@example.com",
        password="securepassword"
    )

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
        "slot_ids": [slot.id],
        "quantity": 2 
    }

    response = client.post(f'http://127.0.0.1:8000/book-class/{user.id}/{fitness_class.id}/', payload, format='json')
    assert response.status_code == 400
    assert "overbooked" in response.json()['error'].lower()
