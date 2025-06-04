"""
Standards models initialization.
All standard-related models are defined in standards.py.
"""

# Import models from the standards.py file (not standard.py)
from .standards import (
    Standard, 
    StandardSection, 
    StandardSubsection,
    StandardAttachment, 
    StandardRevision,
    StandardRequirement,
    StandardComplianceStatus,
    StandardDocument  # Add the missing model here
)

# Define exported models
__all__ = [
    'Standard',
    'StandardSection',
    'StandardSubsection',
    'StandardAttachment',
    'StandardRevision',
    'StandardRequirement',
    'StandardComplianceStatus',
    'StandardDocument'  # Add it to __all__ as well
]
