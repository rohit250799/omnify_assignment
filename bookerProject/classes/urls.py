from django.urls import path

from .views import BookFitnessClassView, BookingListByEmailView, FitnessClassListView, index
urlpatterns = [
    path("", index, name="index"),
    path("classes/", FitnessClassListView.as_view(), name="get_classes"),
    path("book-class/<int:user_id>/<int:fitness_class_id>/", BookFitnessClassView.as_view(), name="book_fitness-]_class"),
    path("bookings/", BookingListByEmailView.as_view(), name="booking_list_by_email"),
]
