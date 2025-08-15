from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

@receiver(post_save, sender=User)
def assign_default_group(sender, instance, created, **kwargs):
    """
    Automatically assign newly created users to the "Standards Viewers" group
    """
    if created:
        # Get or create the default group
        default_group, _ = Group.objects.get_or_create(name="Standards Viewers")
        instance.groups.add(default_group)
