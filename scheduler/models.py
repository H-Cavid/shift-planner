from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('worker', 'Worker'),
        ('manager', 'Manager'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='worker')

    def __str__(self):
        return f"{self.username} ({self.role})"
    
    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = 'manager'
        super().save(*args, **kwargs)



from django.db import models
from django.conf import settings

class Shift(models.Model):
    worker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'worker'},
        related_name='shifts'
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_shifts'
    )

    def __str__(self):
        return f"{self.worker.username} | {self.date} | {self.start_time}–{self.end_time}"
    



# from django.db import models
# from django.conf import settings

# class Availability(models.Model):
#     DAYS_OF_WEEK = [
#         ('Monday', 'Monday'),
#         ('Tuesday', 'Tuesday'),
#         ('Wednesday', 'Wednesday'),
#         ('Thursday', 'Thursday'),
#         ('Friday', 'Friday'),
#         ('Saturday', 'Saturday'),
#         ('Sunday', 'Sunday'),
#     ]

#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     day = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
#     start_time = models.TimeField()
#     end_time = models.TimeField()

#     def __str__(self):
#         return f"{self.user.username} - {self.day} ({self.start_time} - {self.end_time})"

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

class Availability(models.Model):
    worker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='availabilities'
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    note = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date', 'start_time']
        unique_together = ('worker', 'date', 'start_time', 'end_time')

    # def clean(self):
    #     # 1) start before end
    #     if self.start_time >= self.end_time:
    #         raise ValidationError("End time must be after start time.")

    #     # 2) no overlaps for the same worker & date
    #     qs = Availability.objects.filter(worker=self.worker, date=self.date)
    #     if self.pk:
    #         qs = qs.exclude(pk=self.pk)

    #     for other in qs:
    #         if (self.start_time < other.end_time) and (self.end_time > other.start_time):
    #             raise ValidationError("This availability overlaps with an existing one.")

    def __str__(self):
        return f"{self.worker} — {self.date} {self.start_time}-{self.end_time}"


