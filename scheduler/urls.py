from django.urls import path
from .views import register_view, home_view
from django.contrib.auth.views import LogoutView
from .views import my_shifts_view, manager_dashboard, export_shifts_excel

from .views import (
    my_shifts_view,
    MyAvailabilityListView,
    AvailabilityCreateView,
    AvailabilityUpdateView,
    AvailabilityDeleteView,
)

from .views import assign_multiple_shifts_view
from django.contrib.auth.views import LoginView

from .views import export_shifts_pdf, export_my_shifts_pdf, manager_view_availability

from . import views


urlpatterns = [
    path('', home_view, name='home'),  # this is the homepage now
    path('register/', register_view, name='register'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('my-shifts/', my_shifts_view, name='my_shifts'),
    path('manager/', manager_dashboard, name='manager_dashboard'),
    path('assign-multiple-shifts/', assign_multiple_shifts_view, name='assign_multiple_shifts'),
    path('my-availability/', MyAvailabilityListView.as_view(), name='my_availability'),
    path('my-availability/new/', AvailabilityCreateView.as_view(), name='availability_create'),
    path('my-availability/<int:pk>/edit/', AvailabilityUpdateView.as_view(), name='availability_update'),
    path('my-availability/<int:pk>/delete/', AvailabilityDeleteView.as_view(), name='availability_delete'),
    path('export/shifts/excel/', export_shifts_excel, name='export_shifts_excel'),
    path('export/shifts/pdf/', export_shifts_pdf, name='export_shifts_pdf'),
    path('export/my-shifts/excel/', views.export_my_shifts_excel, name='export_my_shifts_excel'),
    path('export/my-shifts/pdf/', export_my_shifts_pdf, name='export_my_shifts_pdf'),  # ← Add this line
    # path('filter-by-date/', views.filter_by_date, name='filter_by_date')
    path('manager/availability/', manager_view_availability, name='manager_view_availability'),

]
