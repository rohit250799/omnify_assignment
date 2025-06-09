
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('class/', include('classes.urls')),
    path('admin/', admin.site.urls),
]
