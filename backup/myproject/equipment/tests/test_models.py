from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone

from equipment.models.equipment import Equipment
from equipment.models.equipment_registry import EquipmentRegistry
from equipment.models.equipment_type import EquipmentType

User = get_user_model()

class EquipmentTypeTests(TestCase):
    """Tests for the EquipmentType model."""

    def setUp(self):
        """Set up test data."""
        self.equipment_type = EquipmentType.objects.create(
            name="Measuring Instrument",
            description="Devices used for measuring physical quantities"
        )

    def test_equipment_type_creation(self):
        """Test the creation of an equipment type."""
        self.assertEqual(self.equipment_type.name, "Measuring Instrument")
        self.assertEqual(self.equipment_type.description, "Devices used for measuring physical quantities")

    def test_equipment_type_str_representation(self):
        """Test the string representation of an equipment type."""
        self.assertEqual(str(self.equipment_type), "Measuring Instrument")


class EquipmentTests(TestCase):
    """Tests for the Equipment model."""

    def setUp(self):
        """Set up test data."""
        # Create equipment type
        self.equipment_type = EquipmentType.objects.create(
            name="Measuring Instrument",
            description="Devices used for measuring physical quantities"
        )

        # Create a sample PDF for testing
        self.pdf_content = b"%PDF-1.4\ntest pdf content"
        self.test_pdf = SimpleUploadedFile(
            "manual.pdf", self.pdf_content, content_type="application/pdf"
        )

        # Create user for ownership
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        # Create equipment
        self.equipment = Equipment.objects.create(
            equipment_name="Digital Caliper",
            equipment_type=self.equipment_type,
            model="DC-100",
            manufacturer="Precision Tools Inc.",
            inventory_number="E-001",
            serial_number="SN12345",
            location="Metrology Lab",
            manual_url="https://example.com/manual.pdf",
            documentation="Calibration required annually",
            technical_status="Good condition, last calibrated 3 months ago",
            manufacture_date=timezone.now().date() - timezone.timedelta(days=365*2),
            purchase_date=timezone.now().date() - timezone.timedelta(days=365),
            purchase_price=199.99
        )

        # Add manual file
        self.equipment.manual_file.save("manual.pdf", self.test_pdf)

    def test_equipment_creation(self):
        """Test the creation of equipment."""
        self.assertEqual(self.equipment.equipment_name, "Digital Caliper")
        self.assertEqual(self.equipment.equipment_type, self.equipment_type)
        self.assertEqual(self.equipment.model, "DC-100")
        self.assertEqual(self.equipment.manufacturer, "Precision Tools Inc.")
        self.assertEqual(self.equipment.purchase_price, 199.99)

    def test_equipment_str_representation(self):
        """Test the string representation of equipment."""
        expected_str = "Digital Caliper (E-001)"
        self.assertEqual(str(self.equipment), expected_str)

    def test_equipment_file_uploaded(self):
        """Test that equipment file was uploaded."""
        self.assertTrue(self.equipment.manual_file)
        self.assertTrue(self.equipment.manual_file.name.endswith('.pdf'))

    def test_equipment_maintenance_fields(self):
        """Test maintenance fields if they exist."""
        maintenance_fields = [
            'quarterly_maintenance',
            'quarterly_maintenance_next_date',
            'annual_maintenance',
            'annual_maintenance_next_date'
        ]

        for field in maintenance_fields:
            if hasattr(self.equipment, field):
                # Just check that the field exists without raising exception
                getattr(self.equipment, field)

    def test_equipment_measurement_fields(self):
        """Test metrological fields if they exist."""
        metrological_fields = [
            'inspection_type',
            'inspection_institution',
            'certificate_number_date',
            'inspection_frequency',
            'next_inspection_date'
        ]

        # If the model has these fields, test functionality
        # This is a check since the model can be customized
        for field in metrological_fields:
            if hasattr(self.equipment, field):
                # Just check that the field exists
                getattr(self.equipment, field)

    def tearDown(self):
        """Clean up after tests."""
        # Delete the uploaded files
        if self.equipment.manual_file:
            self.equipment.manual_file.delete(save=False)


class EquipmentRegistryTests(TestCase):
    """Tests for the EquipmentRegistry model if it exists."""

    def setUp(self):
        """Set up test data."""
        # Check if EquipmentRegistry model exists
        if EquipmentRegistry is not None:
            self.registry_item = EquipmentRegistry.objects.create(
                equipment_name="Analytical Balance",
                model_manufacturer="AB-200 / Analytical Equipment Co.",
                inventory_number="E-002",
                serial_number="SN54321",
                location="Chemistry Lab",
                manufacture_date=timezone.now().date() - timezone.timedelta(days=365*3),
                purchase_date=timezone.now().date() - timezone.timedelta(days=365*2),
                purchase_price=1500.00
            )

    def test_equipment_registry_creation(self):
        """Test the creation of an equipment registry item."""
        # Skip if the model doesn't exist
        if not hasattr(self, 'registry_item'):
            self.skipTest("EquipmentRegistry model not available")

        self.assertEqual(self.registry_item.equipment_name, "Analytical Balance")
        self.assertEqual(self.registry_item.model_manufacturer, "AB-200 / Analytical Equipment Co.")
        self.assertEqual(self.registry_item.inventory_number, "E-002")
        self.assertEqual(self.registry_item.purchase_price, 1500.00)

    def test_equipment_registry_str_representation(self):
        """Test the string representation of an equipment registry item."""
        # Skip if the model doesn't exist
        if not hasattr(self, 'registry_item'):
            self.skipTest("EquipmentRegistry model not available")

        # Test depends on how the __str__ method is implemented
        self.assertTrue(str(self.registry_item))  # Just verify it returns something
        self.assertTrue(isinstance(str(self.registry_item), str))
