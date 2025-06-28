from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Employee, Qualification, Training


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['employee_id', 'first_name', 'last_name', 'position', 'department', 
                  'email', 'phone', 'hire_date', 'is_active', 'notes']
        widgets = {
            'employee_id': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'hire_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'employee_id': _('Employee ID'),
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
            'position': _('Position'),
            'department': _('Department'),
            'email': _('Email'),
            'phone': _('Phone'),
            'hire_date': _('Hire Date'),
            'is_active': _('Active'),
            'notes': _('Notes'),
        }


class QualificationForm(forms.ModelForm):
    class Meta:
        model = Qualification
        fields = ['employee', 'qualification_type', 'description', 'issue_date', 
                  'expiry_date', 'issuing_organization', 'certificate_number', 'document']
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-select'}),
            'qualification_type': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'issue_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'issuing_organization': forms.TextInput(attrs={'class': 'form-control'}),
            'certificate_number': forms.TextInput(attrs={'class': 'form-control'}),
            'document': forms.FileInput(attrs={'class': 'form-control'}),
        }


class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = ['employee', 'training_name', 'description', 'start_date', 'end_date', 
                  'status', 'provider', 'certificate_issued', 'certificate_number', 
                  'certificate_date', 'certificate_document', 'notes']
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-select'}),
            'training_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'provider': forms.TextInput(attrs={'class': 'form-control'}),
            'certificate_issued': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'certificate_number': forms.TextInput(attrs={'class': 'form-control'}),
            'certificate_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'certificate_document': forms.FileInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
