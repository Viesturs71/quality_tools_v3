from django import forms
from django.contrib.auth import get_user_model
from .models import Employee, EmployeeRecord, Qualification, Training, Education

class EmployeeForm(forms.ModelForm):
    """Form for creating and updating employee records."""
    class Meta:
        model = Employee
        fields = [
            'employee_id', 'first_name', 'last_name', 
            'position', 'department', 'email', 'phone',
            'hire_date', 'is_active', 'notes'
        ]
        widgets = {
            'hire_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class EmployeeRecordForm(forms.ModelForm):
    """Form for employee documents and records."""
    class Meta:
        model = EmployeeRecord
        fields = [
            'employee', 'record_type', 'title', 
            'description', 'issue_date', 'expiry_date', 
            'document', 'is_confidential', 'notes'
        ]
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class QualificationForm(forms.ModelForm):
    """Form for employee qualifications."""
    class Meta:
        model = Qualification
        fields = [
            'employee', 'qualification_type', 'description',
            'issue_date', 'expiry_date', 'issuing_organization',
            'certificate_number', 'document'
        ]
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class TrainingForm(forms.ModelForm):
    """Form for employee training records."""
    class Meta:
        model = Training
        fields = [
            'employee', 'training_name', 'description',
            'start_date', 'end_date', 'status', 'provider',
            'certificate_issued', 'certificate_number',
            'certificate_date', 'certificate_document', 'notes'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'certificate_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class EducationForm(forms.ModelForm):
    """Form for employee education background."""
    class Meta:
        model = Education
        fields = [
            'employee', 'institution', 'level',
            'field_of_study', 'degree', 'start_date',
            'end_date', 'is_completed', 'description', 'document'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class UserProfileForm(forms.ModelForm):
    """Form for user profile with personnel data."""
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']
        
    def save(self, commit=True):
        user = super().save(commit=commit)
        # Update the related name if working with the personnel profile
        if hasattr(user, 'personnel_profile'):
            personnel_profile = user.personnel_profile
            if personnel_profile:
                personnel_profile.first_name = user.first_name
                personnel_profile.last_name = user.last_name
                personnel_profile.email = user.email
                if commit:
                    personnel_profile.save()
        return user