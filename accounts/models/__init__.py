"""
Accounts models initialization - make sure imports work correctly with existing code
"""

# This import statement needs to match how the models are actually defined
from .accounts import CustomUser, UserProfile, UserRole, UserPermission

# Make sure any other code that imports from accounts.models will still work
__all__ = ['CustomUser', 'UserProfile', 'UserRole', 'UserPermission']
