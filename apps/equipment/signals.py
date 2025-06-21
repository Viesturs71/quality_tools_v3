from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Equipment

def connect_signals():
    """
    Connect all signals for the equipment app.
    """
    # Example: Connect post_save signal for Equipment
    post_save.connect(equipment_post_save_handler, sender=Equipment)


@receiver(post_save, sender=Equipment)
def equipment_post_save_handler(sender, instance, created, **kwargs):
    if created:
        # Logic for when a new Equipment instance is created
        print(f"New Equipment created: {instance.name}")
