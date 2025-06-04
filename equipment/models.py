"""
Equipment models imports.
This file is kept for backwards compatibility.
The actual models are now in the models directory.
"""
# This file is now deprecated as per project structure requirements.
# All models have been moved to individual files in the models directory.
# Import models from the models package instead.

from .models import (
    EquipmentType,
    Department,
    Equipment,
    EquipmentDocument,
    MaintenanceRecord
)

__all__ = [
    'Equipment',
    'EquipmentDocument',
    'EquipmentType',
    'MaintenanceRecord',
    'Department'  # Added Department to __all__
]


# This file should be deleted or renamed to models_old.py
# All models have been moved to the models/ directory according to project requirements
