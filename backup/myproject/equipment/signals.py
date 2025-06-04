"""
Signals for the *equipment* app.
"""
import logging

from django.apps import apps  # importējām, lai izvairītos no apļveida importiem
from django.db.models.signals import (
    post_delete,
    post_migrate,
    post_save,
    pre_save,
)
from django.dispatch import receiver
from django.utils.text import slugify

logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
# 1. Pēc migrācijām — izveidojam noklusējuma ierakstus
# -----------------------------------------------------------------------------
@receiver(post_migrate)
def create_default_equipment(sender, **kwargs):
    """
    Pēc tam, kad notikušas *equipment* app migrācijas,
    izveido vienu 'Default Equipment Type' un (ja tabula tukša)
    demonstrācijas `Equipment` ierakstu.
    """
    if sender.label != "equipment":          # izpildām tikai savas app migrācijās
        return

    # Saņemam modeļus, izmantojot apps.get_model, lai izvairītos no apļveida importiem
    EquipmentType = apps.get_model("equipment", "EquipmentType")
    Equipment = apps.get_model("equipment", "Equipment")

    try:
        default_type, _ = EquipmentType.objects.get_or_create(
            name="Default Equipment Type",
            defaults={
                "is_measuring_instrument": False,
                "description": "Default equipment type created automatically",
            },
        )

        if not Equipment.objects.exists():
            Equipment.objects.create(
                name="Default Equipment",
                model="Unknown Model",
                manufacturer="Unknown Manufacturer",
                type="Default",
                inventory_number="INV-DEFAULT",
                serial_number="SER-DEFAULT",
                location="Not specified",
                equipment_type=default_type,
            )
            logger.info("✅ Created default equipment and type.")

    # Ja kolonna vai tabula vēl nav, izlaižam – nākamajā `migrate` reizē viss būs kārtībā
    except Exception as exc:
        logger.debug("⏭️  Skipping demo-data creation (likely during first migrate): %s", exc)


# -----------------------------------------------------------------------------
# 2. Pirms saglabāšanas — normalizē inventāra numuru
# -----------------------------------------------------------------------------
@receiver(pre_save, sender=apps.get_model("equipment", "Equipment"))
def format_inventory_number(sender, instance, **kwargs):
    """Ensure inventory number is uppercase and slug-safe."""
    if instance.inventory_number:
        instance.inventory_number = slugify(instance.inventory_number).upper()


# -----------------------------------------------------------------------------
# 3. Žurnāla ieraksti pēc saglabāšanas / dzēšanas
# -----------------------------------------------------------------------------
@receiver(post_save, sender=apps.get_model("equipment", "Equipment"))
def log_equipment_save(sender, instance, created, **kwargs):
    action = "Created" if created else "Updated"
    logger.info(
        "✅ Equipment '%s' %s. (Inventory No: %s)",
        instance.name,
        action,
        instance.inventory_number,
    )


@receiver(post_delete, sender=apps.get_model("equipment", "Equipment"))
def log_equipment_delete(sender, instance, **kwargs):
    logger.warning(
        "🗑️ Equipment '%s' deleted. (Inventory No: %s)",
        instance.name,
        instance.inventory_number,
    )
