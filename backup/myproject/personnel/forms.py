from django import forms

from .models import Employee, Position


class EmployeeForm(forms.ModelForm):
    position = forms.ModelChoiceField(
        queryset=Position.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Izvēlieties amatu",
        label="Amats"
    )

    class Meta:
        model = Employee
        fields = [
            'first_name', 'last_name', 'email',
            'department', 'position', 'hire_date'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'hire_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
