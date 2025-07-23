from apps.documents.utils.document_numbering import (
    generate_document_number,
    validate_document_number_format,
    validate_document_number_uniqueness,
    parse_document_number,
    suggest_next_sequence_number,
)

from django.test import TestCase
from apps.documents.models import (
    Document,
    DocumentSection,
    Attachment,
    DocumentRevision,
)

class DocumentModelTests(TestCase):

    def test_document_number_generation(self):
        """Test document number is generated correctly."""
        document = Document()
        document.save()
        self.assertTrue(document.document_number.startswith('DOC-'))

    def test_document_number_uniqueness(self):
        """Test document number is unique."""
        document1 = Document.objects.create()
        document2 = Document.objects.create()
        self.assertNotEqual(document1.document_number, document2.document_number)

    class DocumentModelTest(TestCase):
        def test_document_creation(self):
            document = Document.objects.create(
                title="Test Document",
                document_number="ABC-QM-01-2023-001",
                version="1.0"
            )
            self.assertEqual(str(document), "ABC-QM-01-2023-001 - Test Document (v1.0)")

class DocumentTest(TestCase):
    def test_document_creation(self):
        document = Document.objects.create(
            title="Test Document",
            document_number="DOC-001",
            version="1.0"
        )
        self.assertEqual(str(document), "DOC-001 - Test Document (v1.0)")

class DocumentAttachmentTest(TestCase):
    def test_attachment_creation(self):
        # First create a document
        document = Document.objects.create(
            title="Test Document",
            document_number="DOC-001",
            version="1.0"
        )
        attachment = Attachment.objects.create(
            document=document,
            description="This is a test attachment."
        )
        self.assertTrue(str(attachment).startswith("Test Document"))

class DocumentRevisionTest(TestCase):
    def test_revision_creation(self):
        from datetime import date
        # First create a document
        document = Document.objects.create(
            title="Test Document",
            document_number="DOC-001",
            version="1.0"
        )
        revision = DocumentRevision.objects.create(
            document=document,
            revision_number="R1",
            revision_date=date.today(),
            description="Initial revision."
        )
        self.assertEqual(str(revision), "R1")