"""
This module re-exports all models from the models package.
"""
from .models.employee import Employee
from .models.qualification import Qualification
from .models.training import Training
from .models.employee_record import EmployeeRecord
from .models.education import Education

# For backward compatibility
__all__ = [
    'Employee',
    'Qualification',
    'Training',
    'EmployeeRecord',
    'Education',
]
