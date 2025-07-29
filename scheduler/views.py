from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth import login
from .forms import CustomUserCreationForm  # use the custom form



def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'worker'  # auto-assign 'worker' role
            user.save()
            login(request, user)
            return redirect('/accounts/login/')  # temporary redirect
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {"form": form})


from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# @login_required
# def home_view(request):
#     return render(request, "home.html", {"user": request.user})

# @login_required
# def home_view(request):
#     if request.user.role == 'manager':
#         return HttpResponse("👔 Welcome Manager")  # Will later change to manager dashboard
#     else:
#         return redirect('my_shifts')  # Redirect workers to their shifts


from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home_view(request):
    return render(request, 'home.html')

# def home_view(request):
#     # Send managers to their dashboard; workers to their home (or shifts)
#     if request.user.role == 'manager':
#         return redirect('manager_dashboard')
#     return render(request, 'home.html')   # worker landing page


@login_required
def manager_dashboard(request):
    return render(request, 'manager/dashboard.html')

from django.contrib.auth.decorators import login_required
from .models import Shift

# @login_required
# def my_shifts_view(request):
#     if request.user.role != 'worker':
#         return redirect('home')  # or raise permission error

#     shifts = Shift.objects.filter(worker=request.user).order_by('date', 'start_time')
#     return render(request, 'my_shifts.html', {'shifts': shifts})

@login_required
def my_shifts_view(request):
    if request.user.role != 'worker':
        return redirect('home')

    shifts = Shift.objects.filter(worker=request.user).order_by('date', 'start_time')

    total_paid = sum(shift.paid_hours() for shift in shifts)
    total_duration = sum(shift.duration_hours() for shift in shifts)

    return render(request, 'my_shifts.html', {
        'shifts': shifts,
        'total_paid': total_paid,
        'total_duration': total_duration
    })




###
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Availability
from .forms import AvailabilityForm

# 🔹 List all availability entries for the current user
class MyAvailabilityListView(LoginRequiredMixin, ListView):
    model = Availability
    template_name = 'availability/my_availabilities.html'
    context_object_name = 'availabilities'

    def get_queryset(self):
        return Availability.objects.filter(worker=self.request.user)






# 🔹 Create availability
class AvailabilityCreateView(LoginRequiredMixin, CreateView):
    model = Availability
    form_class = AvailabilityForm
    template_name = 'availability/availability_form.html'
    success_url = reverse_lazy('my_availability')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['worker'] = self.request.user  # ✅ pass to form
        return kwargs

    def form_valid(self, form):
        form.instance.worker = self.request.user  # ✅ assign before saving
        return super().form_valid(form)


# class AvailabilityCreateView(LoginRequiredMixin, CreateView):
#     model = Availability
#     form_class = AvailabilityForm
#     template_name = 'availability/availability_form.html'
#     success_url = reverse_lazy('my_availability')

#     def form_valid(self, form):
#         form.instance.worker = self.request.user
#         return super().form_valid(form)

# class AvailabilityCreateView(LoginRequiredMixin, CreateView):
#     model = Availability
#     form_class = AvailabilityForm
#     template_name = 'availability/availability_form.html'  # <-- match your template path
#     success_url = reverse_lazy('my_availability')

#     # def get_form_kwargs(self):
#     #     kwargs = super().get_form_kwargs()
#     #     kwargs['worker'] = self.request.user   # pass user to the form for validation
#     #     return kwargs

#     def form_valid(self, form):
#         form.instance.worker = self.request.user
#         return super().form_valid(form)


# 🔹 Edit only own availability
# class AvailabilityUpdateView(LoginRequiredMixin, UpdateView):
#     model = Availability
#     form_class = AvailabilityForm
#     template_name = 'availability/availability_form.html'
#     success_url = reverse_lazy('my_availability')

#     def get_queryset(self):
#         return Availability.objects.filter(worker=self.request.user)

class AvailabilityUpdateView(LoginRequiredMixin, UpdateView):
    model = Availability
    form_class = AvailabilityForm
    template_name = 'availability/availability_form.html'
    success_url = reverse_lazy('my_availability')

    def get_queryset(self):
        return Availability.objects.filter(worker=self.request.user)

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs['worker'] = self.request.user
    #     return kwargs


# 🔹 Delete only own availability
class AvailabilityDeleteView(LoginRequiredMixin, DeleteView):
    model = Availability
    template_name = 'availability/availability_confirm_delete.html'
    success_url = reverse_lazy('my_availability')

    def get_queryset(self):
        return Availability.objects.filter(worker=self.request.user)


from django.forms import modelformset_factory
from django.contrib.admin.views.decorators import staff_member_required
from .models import Shift
from .forms import ShiftForm

@staff_member_required  # only manager/superuser can access
def assign_multiple_shifts_view(request):
    ShiftFormSet = modelformset_factory(Shift, form=ShiftForm, extra=5, can_delete=False)

    if request.method == 'POST':
        formset = ShiftFormSet(request.POST)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for shift in instances:
                shift.created_by = request.user
                shift.save()
            return redirect('home')
    else:
        formset = ShiftFormSet(queryset=Shift.objects.none())  # show empty forms

    return render(request, 'assign_multiple_shifts.html', {'formset': formset})
