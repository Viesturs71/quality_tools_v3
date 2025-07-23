from django.db.models.signals import post_migrate, post_save, pre_save
from django.dispatch import receiver
from .models import Document
from apps.documents.utils.document_numbering import generate_document_number

@receiver(post_migrate)
def create_initial_data(sender, **kwargs):
    """Create initial data after migrations."""
    # Add any initial data creation logic here if needed
    pass

@receiver(post_save, sender=Document)
def generate_document_identifier(sender, instance, created, **kwargs):
    """Generate a document identifier after document creation."""
    if created and not instance.document_number:
        instance.document_number = generate_document_number()
        instance.save()