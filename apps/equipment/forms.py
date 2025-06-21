from django import forms
from .models import Equipment, MaintenanceRecord, EquipmentDocument


class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['name', 'inventory_number', 'status', 'category', 'type', 'location', 'purchase_date', 'warranty_expiry_date', 'notes']


class MaintenanceRecordForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRecord
        fields = ['equipment', 'maintenance_date', 'maintenance_type', 'performed_by', 'description', 'results', 'certificate_number', 'document']


class EquipmentDocumentForm(forms.ModelForm):
    class Meta:
        model = EquipmentDocument
        fields = ['equipment', 'title', 'description', 'uploaded_by', 'document']
