# equipment/serializers.py
from rest_framework import serializers

from .models import (
    Department,
    Equipment,
    EquipmentDocument,
    EquipmentType,
    MaintenanceRecord,
    EquipmentRegistry,
)



class EquipmentRegistrySerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentRegistry
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'code', 'description']

class EquipmentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Equipment model.
    """
    department = DepartmentSerializer(read_only=True)

    class Meta:
        model = Equipment
        fields = [
            'id', 'equipment_name', 'equipment_type', 'model', 'manufacturer',
            'inventory_number', 'serial_number', 'location', 'department',
            'person_responsible', 'manufacture_date', 'purchase_date',
            'purchase_price', 'metrological_control_type',
            'metrological_control_institution', 'certificate_number',
            'certificate_date', 'metrological_control_periodicity',
            'next_verification_date', 'technical_status',
            'additional_information', 'notes', 'created_at', 'updated_at'
        ]

class EquipmentTypeSerializer(serializers.ModelSerializer):
    """
    Serializer for the EquipmentType model.
    """
    class Meta:
        model = EquipmentType
        fields = ['id', 'name', 'requires_metrological_control', 'requires_maintenance']

class EquipmentDocumentSerializer(serializers.ModelSerializer):
    """
    Serializer for the EquipmentDocument model.
    """
    class Meta:
        model = EquipmentDocument
        fields = [
            'id', 'equipment', 'document_type', 'title', 'file',
            'external_url', 'internal_reference', 'description',
            'created_at', 'updated_at'
        ]

class MaintenanceRecordSerializer(serializers.ModelSerializer):
    """
    Serializer for the MaintenanceRecord model.
    """
    class Meta:
        model = MaintenanceRecord
        fields = [
            'id', 'equipment', 'maintenance_type', 'date_performed',
            'performed_by', 'result', 'description', 'next_maintenance_date',
            'created_at', 'updated_at'
        ]
