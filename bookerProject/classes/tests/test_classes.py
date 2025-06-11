import pytest
from django.utils import timezone
from rest_framework.test import APIClient
from classes.models import FitnessClass, AvailableSlot, Bookings, User

@pytest.mark.django_db
def test_get_upcoming_classes():
    now = timezone.now()
    fitness_class = FitnessClass.objects.create(
        name="HIIT",
        date_time=now + timezone.timedelta(days=1),
        instructor="Tyler Robert"
    )
    AvailableSlot.objects.create(
        fitness_class=fitness_class,
        slot_time=fitness_class.date_time,
        capacity=10
    )

    client = APIClient()
    response = client.get('/classes/')

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]['name'] == "HIIT"
    assert 'available_slots' in data[0]

@pytest.mark.django_db
def test_get_bookings_by_email():
    client = APIClient()

    user = User.objects.create(
        name="Test User",
        email="test@example.com",
        password="securepassword"
    )

    fitness_class = FitnessClass.objects.create(
        name="Pilates",
        date_time=timezone.now() + timezone.timedelta(days=1),
        instructor="Sophie"
    )

    slot = AvailableSlot.objects.create(
        fitness_class=fitness_class,
        slot_time=fitness_class.date_time,
        capacity=3
    )

    booking = Bookings.objects.create(
        user=user,  # assumes user with id=1 exists or mock user
        bookedWithMail=user.email,
        fitness_class=fitness_class,
        quantity=1
    )
    booking.slots_booked.add(slot)

    response = client.get('/bookings/?email=test@example.com')
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['bookedWithMail'] == "test@example.com"
