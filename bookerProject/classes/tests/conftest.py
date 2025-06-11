import pytest
#from django.contrib.auth.models import User as django_user
from django.contrib.auth import get_user_model
from classes.models import FitnessClass, AvailableSlot, User
from datetime import datetime, timedelta

@pytest.fixture
def user(db):
    return User.objects.create(
        name="testuser", 
        email="test@mail.com", 
        password="pass1234"
    )

@pytest.fixture
def fitness_class(db):
    return FitnessClass.objects.create(
        name="Yoga Basics",
        date_time=datetime(2025, 6, 20, 18, 0, 0),
        instructor="Alice"
    )

@pytest.fixture
def available_slot(db, fitness_class):
    return AvailableSlot.objects.create(
        fitness_class=fitness_class,
        slot_time=datetime.now(),
        capacity=20
    )
