"""
Signal handlers for the equipment app.
"""
import os
import logging
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from django.apps import apps
from django.conf import settings
from django.utils import timezone
from django.db import transaction
from django.utils.text import slugify

from .models import Equipment, EquipmentDocument, MaintenanceRecord

logger = logging.getLogger(__name__)

def connect_signals():
    """
    Connect signals for equipment models.
    This function is called when the app is ready.
    """
    try:
        Equipment = apps.get_model("equipment", "Equipment")
        
        @receiver(pre_save, sender=Equipment)
        def equipment_pre_save(sender, instance, **kwargs):
            """
            Signal handler for pre-save events on Equipment model.
            Updates the next verification date based on control periodicity if needed.
            """
            # Skip for new objects with no ID yet
            if not instance.pk:
                return
                
            # If this is a measuring instrument with a control_periodicity and certificate_date
            # but no next_verification_date, calculate it
            if (instance.is_measuring_instrument and 
                    instance.control_periodicity and 
                    instance.certificate_date and 
                    not instance.next_verification_date):
                
                # Calculate next verification date based on certificate date and periodicity
                months = instance.control_periodicity
                certificate_date = instance.certificate_date
                
                # Simple calculation: add months to the certificate date
                year = certificate_date.year + ((certificate_date.month - 1 + months) // 12)
                month = ((certificate_date.month - 1 + months) % 12) + 1
                day = min(certificate_date.day, [31, 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1])
                
                instance.next_verification_date = certificate_date.replace(year=year, month=month, day=day)
                logger.info(f"Set next verification date for {instance.name} to {instance.next_verification_date}")

        @receiver(post_save, sender=Equipment)
        def equipment_post_save(sender, instance, created, **kwargs):
            """
            Signal handler for post-save events on Equipment model.
            Creates a directory for equipment documents if it doesn't exist.
            """
            # Create equipment document directory if it doesn't exist
            if created:
                try:
                    equipment_docs_dir = os.path.join(
                        settings.MEDIA_ROOT, 
                        'equipment_docs', 
                        str(instance.id)
                    )
                    os.makedirs(equipment_docs_dir, exist_ok=True)
                    logger.info(f"Created document directory for equipment {instance.name}")
                except Exception as e:
                    logger.error(f"Error creating document directory for equipment {instance.name}: {e}")
                    
        @receiver(pre_delete, sender=EquipmentDocument)
        def delete_equipment_document_file(sender, instance, **kwargs):
            """Delete the file when an EquipmentDocument is deleted."""
            # The actual file deletion logic is in the model's delete method
            # This is just a safety signal in case delete() is bypassed
            if instance.file:
                storage, path = instance.file.storage, instance.file.path
                if storage.exists(path):
                    storage.delete(path)

        @receiver(post_save, sender=MaintenanceRecord)
        def update_equipment_status(sender, instance, created, **kwargs):
            """Update equipment status after maintenance if needed."""
            # This is a placeholder for future automatic status updates
            # For example, if maintenance_type is 'calibration', you might 
            # want to update equipment status to 'operational'
            pass

        # Add more signal handlers here as needed when additional models are implemented

    except (LookupError, ImportError) as e:
        # Models aren't loaded yet, log a message but don't crash
        logger.warning(f"Equipment models not found when loading signals: {e}. This is normal during migrations.")

# Do not connect signals here directly
# Instead, connect them in the app's ready method via connect_signals()
