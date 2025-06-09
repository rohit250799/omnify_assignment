from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import FitnessClass
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
