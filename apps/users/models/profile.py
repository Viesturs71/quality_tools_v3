from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


class Profile(models.Model):
    """User profile model extending the standard Django User model."""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',  # Ensure related_name is 'profile'
        verbose_name=_('User')
    )
    bio = models.TextField(_('Bio'), blank=True, null=True)
    profile_image = models.ImageField(  # Add this field
        _('Profile Image'),
        upload_to='profiles/',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Profils'
        verbose_name_plural = 'Profili'
    
    def __str__(self):
        return f"{self.user.username}'s Profile"


# Signal to create a Profile when a User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a Profile when a new User is created."""
    if created:
        Profile.objects.create(user=instance)


# Signal to save the Profile when the User is saved
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the Profile when the User is saved."""
    if hasattr(instance, 'profile'):
        instance.profile.save()

