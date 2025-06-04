"""
equipment – publiskais API lietošanai ārpus aplikācijas.

Izmantojam 'lazy' __getattr__, lai neizsauktu modeļu importēšanu,
pirms Django aplikāciju reģistrs ir gatavs.
"""

from importlib import import_module
from types import ModuleType
from typing import Any

__all__ = ["Equipment", "EquipmentType", "EquipmentRegistry", "EquipmentDocument", "MaintenanceRecord"]


def _load_models() -> ModuleType:
    """Importē equipment.models tikai pirmajā piekļuvē."""
    return import_module("equipment.models")


def __getattr__(name: str) -> Any:          # pragma: no cover
    if name in __all__:
        return getattr(_load_models(), name)
    raise AttributeError(f"module {__name__!r} has no attribute {name}")

default_app_config = 'equipment.apps.EquipmentConfig'

"""
Quality Tools Project Coding Guidelines

Application Structure
// ...existing code...

Navigation Panel Updates
- Left-side vertical navigation with blue color scheme (#5a8599 to #82a6b7)
- Section headers use uppercase text and darker blue background (#6992a7)
- Collapsible sections with dropdown functionality
- Dropdown indicators (arrow icons) that rotate when expanded
- Current active page highlighted and with left border accent
- Hover effect on menu items (lighter blue background)
- Main sections:
  - DOCUMENTS MANAGEMENT (renamed from QUALITY DOCUMENTS MANAGEMENT)
    - Documents (renamed from Quality Documents)
    - My Documents
    - Standards
    - Documents for Approval
  - EQUIPMENT
    - Equipment Registry
    - Add Equipment
    - Equipment Types
    - Maintenance Schedules
  - PERSONNEL
    - Personnel Directory
    - Qualifications
    - Training Records
  - ADMINISTRATION
    - Admin Panel
    - User Management
    - Company Settings
    - System Configuration
  - AUDITS
    - Upcoming Audits
    - Audit Findings
    - Corrective Actions

Header Style
- Background color: #5a8599 (blue-gray)
- System title: "Management System Tools" 
- Font color: #f5f5e0 (off-white)
- User greeting in uppercase
- Language selector dropdown
- Links for password change and logout

Content Section Styling
- White background with light border
- Section headers in bold
- Form controls with consistent styling
- Buttons with blue background (#5a8599)
- Form groups with proper spacing

"""