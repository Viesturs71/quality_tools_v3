from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


class UserProfile(models.Model):
    """
    User profile model extending the custom Django user.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    department = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Lietotāja profils'
        verbose_name_plural = 'Lietotāju profili'
    
    def __str__(self):
        return f"{self.user.username} profils"


# Signal to create or update user profile when user is created/updated
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    elif hasattr(instance, 'user_profile'):
        instance.user_profile.save()
