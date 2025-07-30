from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email")  # you can add password if needed


# from django import forms
# from .models import Availability

# class AvailabilityForm(forms.ModelForm):
#     class Meta:
#         model = Availability
#         fields = ['date', 'start_time', 'end_time', 'note']
#         widgets = {
#             'date': forms.DateInput(attrs={'type': 'date'}),
#             'start_time': forms.TimeInput(attrs={'type': 'time'}),
#             'end_time': forms.TimeInput(attrs={'type': 'time'}),
#         }
from django import forms
from .models import Availability
from django.core.exceptions import ValidationError

# class AvailabilityForm(forms.ModelForm):
#     class Meta:
#         model = Availability
#         fields = ['date', 'start_time', 'end_time', 'note']
#         widgets = {
#             'date': forms.DateInput(attrs={'type': 'date'}),
#             'start_time': forms.TimeInput(attrs={'type': 'time', 'step': 60}, format='%H:%M'),
#             'end_time': forms.TimeInput(attrs={'type': 'time', 'step': 60}, format='%H:%M'),
#             'note': forms.TextInput(attrs={'placeholder': 'Optional note...'}),
#         }

#     def __init__(self, *args, **kwargs):
#         self.worker = kwargs.pop('worker', None)  # ✅ extract worker safely
#         super().__init__(*args, **kwargs)

#         self.fields['start_time'].input_formats = ['%H:%M']
#         self.fields['end_time'].input_formats = ['%H:%M']

#     def clean(self):
#         cleaned_data = super().clean()
#         date = cleaned_data.get('date')
#         start = cleaned_data.get('start_time')
#         end = cleaned_data.get('end_time')

#         if start and end and start >= end:
#             raise ValidationError("End time must be after start time.")

#         if self.worker and date and start and end:
#             overlaps = Availability.objects.filter(
#                 worker=self.instance.worker,
#                 date=date,
#                 start_time__lt=end,
#                 end_time__gt=start,
#             )
#             if self.instance.pk:
#                 overlaps = overlaps.exclude(pk=self.instance.pk)

#             if overlaps.exists():
#                 raise ValidationError("This availability overlaps with an existing one.")

class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ['date', 'start_time', 'end_time', 'note']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'step': 60}, format='%H:%M'),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'step': 60}, format='%H:%M'),
            # 'note': forms.TextInput(attrs={'placeholder': 'Optional note...'}),
            'note': forms.Textarea(attrs={
                'placeholder': 'Optional note...',
                'rows': 5,
                'style': 'width: 500px; height: 120px; padding: 10px; font-size: 14px; border-radius: 6px;'
            }),
        }

    def __init__(self, *args, **kwargs):
        self.worker = kwargs.pop('worker', None)  # ✅ get from view
        super().__init__(*args, **kwargs)
        self.fields['start_time'].input_formats = ['%H:%M']
        self.fields['end_time'].input_formats = ['%H:%M']

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        start = cleaned_data.get('start_time')
        end = cleaned_data.get('end_time')

        if start and end and start >= end:
            raise ValidationError("End time must be after start time.")

        if self.worker and date and start and end:
            overlaps = Availability.objects.filter(
                worker=self.worker,
                date=date,
                start_time__lt=end,
                end_time__gt=start,
            )
            if self.instance.pk:
                overlaps = overlaps.exclude(pk=self.instance.pk)

            if overlaps.exists():
                raise ValidationError("This availability overlaps with an existing one.")


from django import forms
from .models import Shift

class ShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = ['worker', 'date', 'start_time', 'end_time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }




