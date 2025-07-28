from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Shift,Availability

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'role', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)



# @admin.register(Shift)
# class ShiftAdmin(admin.ModelAdmin):
#     list_display = ['worker', 'date', 'start_time', 'end_time', 'created_by']
#     list_filter = ['date', 'worker']

# @admin.register(Availability)
# class AvailabilityAdmin(admin.ModelAdmin):
#     list_display = ['user', 'day', 'start_time', 'end_time']
#     list_filter = ['day', 'user']

from django.contrib import admin
from .models import Shift, Availability

@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ("worker", "date", "start_time", "end_time", "note", "created_at")
    list_filter = ("date", "worker")
    search_fields = ("worker__username", "worker__first_name", "worker__last_name", "note")

@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ("worker", "date", "start_time", "end_time", "created_by")
    list_filter = ("date", "worker")