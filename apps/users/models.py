"""
This module re-exports all models from the models package.
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()

# Import Profile from models/profile.py instead of defining it here
from .models.profile import Profile
from .models.custom_permission import CustomPermission

# For backward compatibility
__all__ = [
    'Profile',
    'CustomPermission',
]
