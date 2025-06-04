"""
Equipment models package.
"""
from .department import Department
from .equipment import Equipment
from .equipment_document import EquipmentDocument
from .equipment_type import EquipmentType
from .maintenance_record import MaintenanceRecord

__all__ = [
    'Department',
    'Equipment',
    'EquipmentDocument',
    'EquipmentType',
    'MaintenanceRecord',
]
