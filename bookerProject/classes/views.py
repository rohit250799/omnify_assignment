from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import FitnessClass, Bookings

import json
# Create your views here.

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

def book_class(request):
    if request.method != "POST": return JsonResponse({'error': 'Only POST request is allowed'}, status=405)

    body = json.loads(request.body)
    fitnessClass_id = body.get('id')
    bookerName = body.get('name')
    bookerEmail = body.get('email')

    if not all([fitnessClass_id, bookerName, bookerEmail]):
        return JsonResponse({'error': 'Required fields missing'}, status=400)
    
    fitness_class = FitnessClass.objects.all(id=fitnessClass_id)
    availableSlot = None

    for slot in fitness_class.slots.all():
        if slot.available_count() > 0:
            availableSlot = slot
            break

    if not availableSlot: return JsonResponse({'error': 'Slot not available in the program'}, status=400)

    #creating the booking
    Bookings.objects.create(
        user_name=bookerName,
        user_email=bookerEmail,
        fitness_class=fitness_class,
        slot=availableSlot
    )

    return JsonResponse({'success': f'Booking confirmed for {bookerName} in {fitness_class.name} at {availableSlot.slot_time}'})


