"""
Equipment models initialization.

This file imports and exposes all models from the equipment app
to make them available through the 'equipment.models' namespace.
"""
from .equipment import (
    Department,
    Equipment,
    EquipmentType,
    EquipmentDocument,
    MaintenanceRecord,
    EquipmentRegistry,
)

__all__ = [
    'Department',
    'Equipment',
    'EquipmentType',
    'EquipmentDocument',
    'MaintenanceRecord',
    'EquipmentRegistry',
]
