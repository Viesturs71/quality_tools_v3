from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Equipment, EquipmentDocument, MaintenanceRecord


class EquipmentForm(forms.ModelForm):
    """
    Form for adding and editing equipment.
    """
    class Meta:
        model = Equipment
        fields = [
            'equipment_name', 'equipment_type', 'model', 'manufacturer',
            'inventory_number', 'serial_number', 'location', 'department',
            'person_responsible', 'manufacture_date', 'purchase_date',
            'purchase_price', 'metrological_control_type',
            'metrological_control_institution', 'certificate_number',
            'certificate_date', 'metrological_control_periodicity',
            'next_verification_date', 'technical_status',
            'additional_information', 'notes'
        ]
        widgets = {
            'manufacture_date': forms.DateInput(attrs={'type': 'date'}),
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
            'certificate_date': forms.DateInput(attrs={'type': 'date'}),
            'next_verification_date': forms.DateInput(attrs={'type': 'date'}),
            'additional_information': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make certain fields required based on equipment type
        if self.instance and self.instance.equipment_type and self.instance.equipment_type.requires_metrological_control:
            self.fields['metrological_control_type'].required = True
            self.fields['metrological_control_institution'].required = True
            self.fields['certificate_number'].required = True
            self.fields['certificate_date'].required = True
            self.fields['metrological_control_periodicity'].required = True
            self.fields['next_verification_date'].required = True


class EquipmentDocumentForm(forms.ModelForm):
    """
    Form for adding and editing equipment documents.
    """
    class Meta:
        model = EquipmentDocument
        fields = ['document_type', 'title', 'file', 'external_url', 'internal_reference', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            # Check file size (max 1MB)
            if file.size > 1024 * 1024:
                raise forms.ValidationError(_('File size must be no more than 1MB'))
            # Check file type
            if not file.name.endswith('.pdf'):
                raise forms.ValidationError(_('Only PDF files are allowed'))
        return file


class MaintenanceRecordForm(forms.ModelForm):
    """
    Form for adding and editing maintenance records.
    """
    class Meta:
        model = MaintenanceRecord
        fields = ['maintenance_type', 'date_performed', 'performed_by', 'result', 'description', 'next_maintenance_date']
        widgets = {
            'date_performed': forms.DateInput(attrs={'type': 'date'}),
            'next_maintenance_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
