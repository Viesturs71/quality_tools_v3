#quality_docs/signals.py
from django.db.models.signals import post_migrate, post_save, pre_save
from django.dispatch import receiver

from quality_docs.models.company import Company
from quality_docs.models.documents import QualityDocument


@receiver(post_migrate)
def create_default_company(sender, **kwargs):
    """Pēc migrācijas izveido noklusēto uzņēmumu, ja tāda nav."""
    if sender.name == "quality_docs":
        company, created = Company.objects.get_or_create(
            name="Test Company",
            defaults={"identifier": "TC"},
        )
        if created:
            pass
        else:
            pass


@receiver(pre_save, sender=Company)
def format_company_identifier(sender, instance, **kwargs):
    """Pirms saglabāšanas nodrošina, ka uzņēmuma identifikators ir lieliem burtiem."""
    if instance.identifier:
        instance.identifier = instance.identifier.upper()


@receiver(post_save, sender=QualityDocument)
def generate_document_identifier(sender, instance, created, **kwargs):
    """Pēc dokumenta izveides ģenerē identifikatoru, ja tā nav."""
    if created and not instance.document_identifier:
        instance.generate_document_identifier()
        instance.save()

@receiver(post_save, sender=Standard)
def standard_post_save(sender, instance, created, **kwargs):
    # Your signal logic here
    pass

@receiver(post_save, sender=StandardSection)
def standard_section_post_save(sender, instance, created, **kwargs):
    # Your signal logic here
    pass
