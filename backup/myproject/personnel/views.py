#personnel/views.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import EmployeeForm
from .models import Employee


class EmployeeListView(LoginRequiredMixin, ListView):
    model = Employee
    template_name = 'personnel/employee_list.html'
    context_object_name = 'employees'

class EmployeeDetailView(LoginRequiredMixin, DetailView):
    model = Employee
    template_name = 'personnel/employee_detail.html'

class EmployeeCreateView(LoginRequiredMixin, CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'personnel/employee_form.html'
    success_url = reverse_lazy('personnel:employee_list')

class EmployeeUpdateView(LoginRequiredMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'personnel/employee_form.html'
    success_url = reverse_lazy('personnel:employee_list')

class EmployeeDeleteView(LoginRequiredMixin, DeleteView):
    model = Employee
    template_name = 'personnel/employee_confirm_delete.html'
    success_url = reverse_lazy('personnel:employee_list')

@login_required
def personnel_list(request):
    """Display list of personnel"""
    return render(request, 'personnel/personnel_list.html', {
        'page_title': 'Personnel Registry'
    })
