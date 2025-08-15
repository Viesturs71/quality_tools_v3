"""
This module re-exports all models from the models package.
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


class Profile(models.Model):
    """User profile model linked to the custom Django user."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='users_profile')
    bio = models.TextField(max_length=500, blank=True)
    profile_image = models.ImageField(upload_to='profile_pics', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return f"{self.user.username}'s profile"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'users_profile'):
        instance.users_profile.save()


from .models.custom_permission import CustomPermission

# For backward compatibility
__all__ = [
    'Profile',
    'CustomPermission',
]
