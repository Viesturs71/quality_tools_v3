#['equipment/forms.py']
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Equipment, EquipmentDocument, MaintenanceRecord, EquipmentRegistry

class EquipmentForm(forms.ModelForm):
    """Form for creating and updating equipment records."""
    
    class Meta:
        model = Equipment
        fields = [
            # General Information
            'name', 'equipment_type', 'model', 'type_details', 'manufacturer',
            'inventory_number', 'serial_number', 'location',
            
            # Department Information
            'department', 'responsible_person',
            
            # Dates and Financial Information
            'manufacture_date', 'purchase_date', 'purchase_price',
            
            # Metrological Control (for measuring instruments)
            'is_measuring_instrument', 'metrological_control_type',
            'metrological_control_institution', 'certificate_number',
            'certificate_date', 'control_periodicity', 'next_verification_date',
            
            # Status Information
            'status', 'additional_info', 'notes',
        ]
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'px-4 py-2 border border-gray-300 rounded'}),
            'model': forms.TextInput(attrs={'class': 'px-4 py-2 border border-gray-300 rounded'}),
            'type_details': forms.TextInput(attrs={'class': 'px-4 py-2 border border-gray-300 rounded'}),
            'manufacturer': forms.TextInput(attrs={'class': 'px-4 py-2 border border-gray-300 rounded'}),
            'inventory_number': forms.TextInput(attrs={'class': 'px-4 py-2 border border-gray-300 rounded'}),
            'serial_number': forms.TextInput(attrs={'class': 'px-4 py-2 border border-gray-300 rounded'}),
            'location': forms.TextInput(attrs={'class': 'px-4 py-2 border border-gray-300 rounded'}),
            'responsible_person': forms.TextInput(attrs={'class': 'px-4 py-2 border border-gray-300 rounded'}),
            'manufacture_date': forms.DateInput(attrs={'class': 'px-4 py-2 border border-gray-300 rounded', 'type': 'date'}),
            'purchase_date': forms.DateInput(attrs={'class': 'px-4 py-2 border border-gray-300 rounded', 'type': 'date'}),
            'purchase_price': forms.NumberInput(attrs={'class': 'px-4 py-2 border border-gray-300 rounded'}),
            'metrological_control_type': forms.TextInput(attrs={'class': 'px-4 py-2 border border-gray-300 rounded'}),
            'metrological_control_institution': forms.TextInput(attrs={'class': 'px-4 py-2 border border-gray-300 rounded'}),
            'certificate_number': forms.TextInput(attrs={'class': 'px-4 py-2 border border-gray-300 rounded'}),
            'certificate_date': forms.DateInput(attrs={'class': 'px-4 py-2 border border-gray-300 rounded', 'type': 'date'}),
            'control_periodicity': forms.NumberInput(attrs={'class': 'px-4 py-2 border border-gray-300 rounded'}),
            'next_verification_date': forms.DateInput(attrs={'class': 'px-4 py-2 border border-gray-300 rounded', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'px-4 py-2 border border-gray-300 rounded'}),
            'notes': forms.Textarea(attrs={'class': 'px-4 py-2 border border-gray-300 rounded', 'rows': 3}),
            'additional_info': forms.Textarea(attrs={'class': 'px-4 py-2 border border-gray-300 rounded', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add the required field indicator (asterisk)
        for field_name in ['name', 'inventory_number', 'serial_number', 'location']:
            self.fields[field_name].label = f"{self.fields[field_name].label} *"
        
        # Add JavaScript to show/hide metrological control fields based on is_measuring_instrument
        self.fields['is_measuring_instrument'].widget.attrs.update({
            'class': 'px-4 py-2 border border-gray-300 rounded',
            'onchange': 'toggleMetrologicalFields(this.checked)'
        })

class EquipmentDocumentForm(forms.ModelForm):
    """Form for uploading equipment documentation."""
    class Meta:
        model = EquipmentDocument
        fields = [
            'equipment',
            'document',
            'external_url',
            'document_type',
            'internal_reference',
            'description',
        ]
        widgets = {
            'document_type': forms.Select(attrs={'class': 'px-4 py-2 border border-gray-300 rounded'}),
            'title': forms.TextInput(attrs={'class': 'px-4 py-2 border border-gray-300 rounded'}),
            'file': forms.FileInput(attrs={'class': 'px-4 py-2 border border-gray-300 rounded'}),
            'external_url': forms.URLInput(attrs={'class': 'px-4 py-2 border border-gray-300 rounded'}),
            'internal_reference': forms.TextInput(attrs={'class': 'px-4 py-2 border border-gray-300 rounded'}),
            'description': forms.Textarea(attrs={'class': 'px-4 py-2 border border-gray-300 rounded', 'rows': 3}),
        }
        
    def clean_file(self):
        """Validate that the uploaded file is a PDF and not too large."""
        file = self.cleaned_data.get('file', False)
        if file:
            # Check file type
            if not file.name.endswith('.pdf'):
                raise forms.ValidationError(_("Only PDF files are allowed."))
            
            # Check file size (1MB = 1048576 bytes)
            if file.size > 1048576:
                raise forms.ValidationError(_("File size must be under 1MB."))
        return file

class MaintenanceRecordForm(forms.ModelForm):
    """Form for creating and updating maintenance records."""
    class Meta:
        model = MaintenanceRecord
        fields = ['maintenance_date', 'maintenance_type', 'performed_by', 'description', 'next_maintenance_date']
        widgets = {
            'maintenance_date': forms.DateInput(attrs={'class': 'px-4 py-2 border border-gray-300 rounded', 'type': 'date'}),
            'maintenance_type': forms.Select(attrs={'class': 'px-4 py-2 border border-gray-300 rounded'}),
            'performed_by': forms.TextInput(attrs={'class': 'px-4 py-2 border border-gray-300 rounded'}),
            'description': forms.Textarea(attrs={'class': 'px-4 py-2 border border-gray-300 rounded', 'rows': 3}),
            'next_maintenance_date': forms.DateInput(attrs={'class': 'px-4 py-2 border border-gray-300 rounded', 'type': 'date'}),
        }

class EquipmentRegistryForm(forms.ModelForm):
    class Meta:
        model = EquipmentRegistry
        fields = ['equipment', 'authorized_since', 'notes']