from apps.documents.utils.document_numbering import (
    generate_document_number,
    validate_document_number_format,
    validate_document_number_uniqueness,
    parse_document_number,
    suggest_next_sequence_number,
)

from django.test import TestCase
from apps.documents.models import (
    QualityDocument,
    DocumentSection,
    DocumentAttachment,
    DocumentRevision,
)

class DocumentModelTests(TestCase):

    def test_document_number_generation(self):
        """Test document number is generated correctly."""
        document = QualityDocument()
        document.save()
        self.assertTrue(document.document_number.startswith('DOC-'))

    def test_document_number_uniqueness(self):
        """Test document number is unique."""
        document1 = QualityDocument.objects.create()
        document2 = QualityDocument.objects.create()
        self.assertNotEqual(document1.document_number, document2.document_number)

    class QualityDocumentModelTest(TestCase):
        def test_document_creation(self):
            document = QualityDocument.objects.create(
                title="Test Document",
                document_number="ABC-QM-01-2023-001",
                version="v1.0"
            )
            self.assertEqual(str(document), "ABC-QM-01-2023-001: Test Document")

class QualityDocumentTest(TestCase):
    def test_document_creation(self):
        document = QualityDocument.objects.create(
            title="Test Document",
            document_number="DOC-001",
            version="v1.0"
        )
        self.assertEqual(str(document), "DOC-001: Test Document")

class DocumentAttachmentTest(TestCase):
    def test_attachment_creation(self):
        attachment = DocumentAttachment.objects.create(
            title="Test Attachment",
            description="This is a test attachment."
        )
        self.assertEqual(str(attachment), "Test Attachment")

class DocumentRevisionTest(TestCase):
    def test_revision_creation(self):
        revision = DocumentRevision.objects.create(
            revision_number="R1",
            description="Initial revision."
        )
        self.assertEqual(str(revision), "R1")