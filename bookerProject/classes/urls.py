from django.urls import path

from .views import BookFitnessClassView, index, get_classes

urlpatterns = [
    path("", index, name="index"),
    path("classes/", get_classes, name="get_classes"),
    path("book-class/<int:user_id>/<int:fitness_class_id>/", BookFitnessClassView.as_view(), name="book_fitness-]_class"),
]
