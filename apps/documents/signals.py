from django.db.models.signals import post_migrate, post_save, pre_save
from django.dispatch import receiver
from .models import Company, QualityDocument
from apps.documents.utils.document_numbering import generate_document_number

@receiver(post_migrate)
def create_default_company(sender, **kwargs):
    """Create a default company after migrations."""
    if sender.name == "apps.documents":
        Company.objects.get_or_create(
            name="Test Company",
            defaults={"identifier": "TC"},
        )

@receiver(pre_save, sender=Company)
def format_company_identifier(sender, instance, **kwargs):
    """Ensure the company identifier is uppercase before saving."""
    if instance.identifier:
        instance.identifier = instance.identifier.upper()

@receiver(post_save, sender=QualityDocument)
def generate_document_identifier(sender, instance, created, **kwargs):
    """Generate a document identifier after document creation."""
    if created and not instance.document_number:
        instance.document_number = f"Generated-{instance.pk}"
        instance.save()