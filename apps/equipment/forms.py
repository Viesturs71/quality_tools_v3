from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Equipment, MaintenanceRecord, EquipmentDocument, CalibrationRecord


class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = [
            'name', 
            'equipment_type', 
            'inventory_number', 
            'department', 
            'responsible_person',
            'status',
            'description',
            'manufacturer',
            'model_number',
            'serial_number',
            'purchase_date',
            'needs_calibration',
            'calibration_frequency',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
        }


class MaintenanceRecordForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRecord
        fields = [
            'equipment', 
            'maintenance_type', 
            'performed_by', 
            'performed_date', 
            'description', 
            'actions_taken', 
            'parts_replaced',
            'next_maintenance_date'
        ]
        widgets = {
            'performed_date': forms.DateInput(attrs={'type': 'date'}),
            'next_maintenance_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'actions_taken': forms.Textarea(attrs={'rows': 3}),
        }


class CalibrationRecordForm(forms.ModelForm):
    class Meta:
        model = CalibrationRecord
        fields = [
            'equipment', 
            'performed_by', 
            'calibration_date', 
            'certificate_number', 
            'description', 
            'results',
            'passed',
            'next_calibration_date'
        ]
        widgets = {
            'calibration_date': forms.DateInput(attrs={'type': 'date'}),
            'next_calibration_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'results': forms.Textarea(attrs={'rows': 3}),
        }


class EquipmentDocumentForm(forms.ModelForm):
    class Meta:
        model = EquipmentDocument
        fields = ['equipment', 'title', 'description', 'document']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
