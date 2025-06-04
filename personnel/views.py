from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Employee, EmployeeRecord, Qualification, Training, Education
from .forms import (
    EmployeeForm, 
    EmployeeRecordForm, 
    QualificationForm, 
    TrainingForm, 
    EducationForm
)

# Employee views
@login_required
def employee_list(request):
    """Display a list of employees."""
    search_query = request.GET.get('search', '')
    employees = Employee.objects.all()
    
    if search_query:
        employees = employees.filter(
            Q(first_name__icontains=search_query) | 
            Q(last_name__icontains=search_query) |
            Q(employee_id__icontains=search_query) |
            Q(position__icontains=search_query)
        )
    
    # Filter by department if specified
    department_id = request.GET.get('department')
    if department_id:
        employees = employees.filter(department_id=department_id)
    
    # Filter by active status if specified
    active_filter = request.GET.get('is_active')
    if active_filter == 'true':
        employees = employees.filter(is_active=True)
    elif active_filter == 'false':
        employees = employees.filter(is_active=False)
    
    # Pagination
    paginator = Paginator(employees, 20)  # Show 20 employees per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    
    return render(request, 'personnel/employee_list.html', context)

@login_required
def employee_detail(request, pk):
    """Display detailed information about an employee."""
    employee = get_object_or_404(Employee, pk=pk)
    
    context = {
        'employee': employee,
        'qualifications': employee.qualifications.all(),
        'trainings': employee.training_records.all(),
        'employee_records': employee.employee_records.all(),
        'educations': employee.education.all(),
    }
    
    return render(request, 'personnel/employee_detail.html', context)

@login_required
def employee_create(request):
    """Create a new employee record."""
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save()
            messages.success(request, _("Employee record created successfully."))
            return redirect('personnel:employee_detail', pk=employee.pk)
    else:
        form = EmployeeForm()
    
    return render(request, 'personnel/employee_form.html', {'form': form, 'is_create': True})

@login_required
def employee_update(request, pk):
    """Update an existing employee record."""
    employee = get_object_or_404(Employee, pk=pk)
    
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, _("Employee record updated successfully."))
            return redirect('personnel:employee_detail', pk=employee.pk)
    else:
        form = EmployeeForm(instance=employee)
    
    return render(request, 'personnel/employee_form.html', {'form': form, 'employee': employee, 'is_create': False})

@login_required
@permission_required('personnel.change_employee', raise_exception=True)
def employee_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'personnel/employee_form.html', {'form': form})

@login_required
@permission_required('personnel.add_trainingparticipation', raise_exception=True)
def register_training(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    if request.method == 'POST':
        form = EmployeeRecordForm(request.POST, request.FILES)
        if form.is_valid():
            training = form.save(commit=False)
            training.employee = employee
            training.save()
            return redirect('employee_list')
    else:
        form = EmployeeRecordForm()
    return render(request, 'personnel/register_training.html', {'form': form, 'employee': employee})

def get_employee_from_user(user):
    """Get the employee profile for a user."""
    try:
        return user.personnel_profile  # Updated from employee_profile
    except Employee.DoesNotExist:
        return None

@login_required
def index(request):
    """Personnel management main page"""
    context = {
        'title': 'Personnel Management',
    }
    return render(request, 'personnel/index.html', context)

@login_required
def staff_list(request):
    """View for listing staff members"""
    context = {
        'title': 'Staff Records',
    }
    return render(request, 'personnel/staff_list.html', context)

@login_required
def staff_detail(request, staff_id):
    """View for a specific staff member's details"""
    context = {
        'title': 'Staff Details',
        'staff_id': staff_id,
    }
    return render(request, 'personnel/staff_detail.html', context)

@login_required
def qualification_list(request):
    """View for listing qualifications"""
    context = {
        'title': 'Qualifications',
    }
    return render(request, 'personnel/qualification_list.html', context)

@login_required
def qualification_detail(request, qualification_id):
    """View for a specific qualification's details"""
    context = {
        'title': 'Qualification Details',
        'qualification_id': qualification_id,
    }
    return render(request, 'personnel/qualification_detail.html', context)

@login_required
def training_list(request):
    """View for listing training records"""
    context = {
        'title': 'Training Records',
    }
    return render(request, 'personnel/training_list.html', context)

@login_required
def training_detail(request, training_id):
    """View for a specific training record's details"""
    context = {
        'title': 'Training Details',
        'training_id': training_id,
    }
    return render(request, 'personnel/training_detail.html', context)
