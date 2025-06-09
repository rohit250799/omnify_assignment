from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("classes/", views.get_classes, name="get_classes"),
]