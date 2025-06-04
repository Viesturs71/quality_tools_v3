from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group

@receiver(post_save, sender=User)
def assign_default_group(sender, instance, created, **kwargs):
    if created:
        # Piemērs – visiem jaunajiem piešķir "Standards Viewers"
        default_group, _ = Group.objects.get_or_create(name="Standards Viewers")
        instance.groups.add(default_group)
