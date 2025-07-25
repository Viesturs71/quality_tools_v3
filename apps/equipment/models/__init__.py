from .equipment import Equipment
from .equipment_type import EquipmentType
from .equipment_document import EquipmentDocument
from .maintenance import MaintenanceRecord  # Use this model instead of maintenance_record.py
from .equipment_category import EquipmentCategory
from .department import Department
from .equipment_registry import EquipmentRegistry
from .calibration import CalibrationRecord

__all__ = [
    'Equipment',
    'EquipmentType',
    'EquipmentDocument',
    'MaintenanceRecord',
    'EquipmentCategory',
    'Department',
    'EquipmentRegistry',
    'CalibrationRecord',
]
