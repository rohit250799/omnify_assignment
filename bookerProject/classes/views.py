from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db import models

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import FitnessClass, Bookings, User as appUser, AvailableSlot
from .serializers import BookingSerializer

import json


class BookFitnessClassView(APIView):
    def post(self, request, user_id, fitness_class_id):
        slot_ids = request.data.get('slot_ids')
        quantity = request.data.get('quantity', 1)

        if not slot_ids or not isinstance(slot_ids, list):
            return Response({'error': 'slot_ids must be a list of slot IDs'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = appUser.objects.get(pk=user_id)
            fitness_class = FitnessClass.objects.get(pk=fitness_class_id)
            slots = AvailableSlot.objects.filter(id__in=slot_ids, fitness_class=fitness_class).distinct()
        except appUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except FitnessClass.DoesNotExist:
            return Response({'error': 'Fitness class not found'}, status=status.HTTP_404_NOT_FOUND)
        
        valid_slot_ids = list(slots.values_list('id', flat=True))
        print("Expected Slot IDs:", slot_ids)
        print("Valid Slot IDs:", valid_slot_ids)

        # Ensure all slots exist
        if slots.count() != len(slot_ids):
            return Response({'error': 'One or more slot_ids are invalid for this class'}, status=status.HTTP_400_BAD_REQUEST)

        for slot in slots:
            current_bookings = Bookings.objects.filter(slots_booked=slot).aggregate(total=models.Sum('quantity'))['total'] or 0
            if current_bookings + quantity > slot.capacity:
                return Response(
                    {'error': f'Slot {slot.id} is full or overbooked. Only {slot.capacity - current_bookings} remaining.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Create booking
        booking = Bookings.objects.create(
            user=user,
            bookedWithMail=user.email,
            fitness_class=fitness_class,
            quantity=quantity
        )
        booking.slots_booked.set(slots)
        booking.save()

        serializer = BookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class BookingListByEmailView(APIView):
    def get(self, request):
        email = request.query_params.get('email')
        if not email: return Response({'error': 'Email not provided'}, status=status.HTTP_400_BAD_REQUEST)

        bookings = Bookings.objects.filter(bookedWithMail=email)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

def index(request):
    return HttpResponse("Hello, you reached the classes index")

def get_classes(request):
    if request.method == "GET":
        fitnessClasses = FitnessClass.objects.all()
        returnData = []

    for fitness_class in fitnessClasses:
        returnData.append({
            "id": fitness_class.id,
            "name": fitness_class.name,
            "date_time": fitness_class.date_time,
            "instructor": fitness_class.instructor
        })

    return JsonResponse(returnData, safe=False)