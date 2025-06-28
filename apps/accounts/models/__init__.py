"""
Models package for the accounts app.
"""

# Import models from their respective files
from .user import CustomUser
from .user_profile import UserProfile
from .user_permissions import UserPermission

# Export models for easier imports elsewhere
__all__ = [
    'CustomUser',
    'UserProfile',
    'UserPermission',
]
