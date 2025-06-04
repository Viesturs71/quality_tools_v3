# equipment/resources.py
from import_export import resources

from .equipment_registry import EquipmentRegistry


class EquipmentRegistryResource(resources.ModelResource):
    """Resource for managing import/export of equipment data."""

    class Meta:
        model = EquipmentRegistry
        fields = (
            "id",
            "equipment_name",
            "model_manufacturer",
            "inventory_number",
            "serial_number",
            "location",
            "inspection_type",
            "inspection_institution",
            "certificate_number_date",
            "inspection_frequency",
            "next_inspection_date",
        )
        export_order = fields
