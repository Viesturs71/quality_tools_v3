from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Employee
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


class EmployeeListView(ListView):
    model = Employee
    template_name = 'personnel/employee_list.html'
    context_object_name = 'employees'


class EmployeeDetailView(DetailView):
    model = Employee
    template_name = 'personnel/employee_detail.html'


class EmployeeCreateView(CreateView):
    model = Employee
    fields = ['employee_id', 'first_name', 'last_name', 'position', 'department', 'email', 'phone', 'hire_date', 'is_active', 'notes']
    template_name = 'personnel/employee_form.html'
    success_url = reverse_lazy('personnel:employee_list')


class EmployeeUpdateView(UpdateView):
    model = Employee
    fields = ['employee_id', 'first_name', 'last_name', 'position', 'department', 'email', 'phone', 'hire_date', 'is_active', 'notes']
    template_name = 'personnel/employee_form.html'
    success_url = reverse_lazy('personnel:employee_list')


class EmployeeDeleteView(DeleteView):
    model = Employee
    template_name = 'personnel/employee_confirm_delete.html'
    success_url = reverse_lazy('personnel:employee_list')


def personnel_list(request):
    """View to list personnel information."""
    return render(request, 'personnel/personnel_list.html')


@login_required
def my_profile(request):
    """View for displaying the user's personnel profile."""
    return render(request, 'personnel/my_profile.html', {'page_title': 'My Profile'})


@login_required
def my_trainings(request):
    """View for displaying the user's training records."""
    return render(request, 'personnel/my_trainings.html', {'page_title': 'My Trainings'})


@login_required
def my_qualifications(request):
    """View for displaying the user's qualifications."""
    return render(request, 'personnel/my_qualifications.html', {'page_title': 'My Qualifications'})
