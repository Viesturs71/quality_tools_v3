"""
Equipment models imports.
This file is kept for backwards compatibility.
The actual models are now in the models directory.
"""
from .models.equipment import Equipment
from .models.equipment_document import EquipmentDocument
from .models.equipment_type import EquipmentType
from .models.maintenance_record import MaintenanceRecord

__all__ = [
    'Equipment',
    'EquipmentDocument',
    'EquipmentType',
    'MaintenanceRecord'
]
