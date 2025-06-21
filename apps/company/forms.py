from django import forms
from .models import Company, Department, Location


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'registration_number', 'identifier', 'address', 'city', 'state_province', 'country', 'postal_code', 'email', 'phone', 'website', 'is_active']


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'code', 'company', 'description', 'is_active']


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'address', 'city', 'postal_code', 'country', 'company', 'is_active']
