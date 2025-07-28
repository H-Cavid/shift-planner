from django.urls import path
from .views import register_view, home_view
from django.contrib.auth.views import LogoutView
from .views import my_shifts_view

from .views import (
    my_shifts_view,
    MyAvailabilityListView,
    AvailabilityCreateView,
    AvailabilityUpdateView,
    AvailabilityDeleteView,
)





urlpatterns = [
    path('', home_view, name='home'),  # this is the homepage now
    path('register/', register_view, name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('my-shifts/', my_shifts_view, name='my_shifts'),
    path('my-availability/', MyAvailabilityListView.as_view(), name='my_availability'),
    path('my-availability/new/', AvailabilityCreateView.as_view(), name='availability_create'),
    path('my-availability/<int:pk>/edit/', AvailabilityUpdateView.as_view(), name='availability_update'),
    path('my-availability/<int:pk>/delete/', AvailabilityDeleteView.as_view(), name='availability_delete')
]
