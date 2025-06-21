from django import forms
from .models import Employee, Qualification, Training


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['employee_id', 'first_name', 'last_name', 'position', 'department', 'email', 'phone', 'hire_date', 'is_active', 'notes']


class QualificationForm(forms.ModelForm):
    class Meta:
        model = Qualification
        fields = ['employee', 'qualification_type', 'description', 'issue_date', 'expiry_date', 'issuing_organization', 'certificate_number', 'document']


class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = ['employee', 'training_name', 'description', 'start_date', 'end_date', 'status', 'provider', 'certificate_issued', 'certificate_number', 'certificate_date', 'certificate_document', 'notes']
