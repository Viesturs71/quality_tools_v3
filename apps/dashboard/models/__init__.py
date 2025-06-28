# apps/dashboard/models/__init__.py

from .user_preference import UserPreference
from .user_widget_position import UserWidgetPosition
from .widget import Widget

__all__ = (
    "UserPreference",
    "UserWidgetPosition",
    "Widget",
)
