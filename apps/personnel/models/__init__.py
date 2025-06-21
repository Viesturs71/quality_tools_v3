"""
Personnel models initialization.
"""

from .employee import Employee
from .qualification import Qualification
from .training import Training
from .employee_record import EmployeeRecord
from .education import Education

__all__ = [
    'Employee',
    'Qualification',
    'Training',
    'EmployeeRecord',
    'Education',
]

