#quality_docs/tests.py
import datetime

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from quality_docs.forms import QualityDocumentForm
from quality_docs.models.approval_flow import ApprovalFlow
from quality_docs.models.company import Company
from quality_docs.models.documents import DocumentType, QualityDocument

User = get_user_model()


class QualityDocumentModelTest(TestCase):
    """Testē QualityDocument modeļa funkcionalitāti."""

    @classmethod
    def setUpTestData(cls):
        cls.company = Company.objects.create(name="Test Company", identifier="TC")
        cls.doc_type = DocumentType.objects.create(name="Procedūra", identifier="PROC")
        cls.user = User.objects.create_user(username="testuser", password="password")
        cls.document = QualityDocument.objects.create(
            company=cls.company,
            document_type=cls.doc_type,
            title="Testa dokuments",
            version="v01.00",
            review_date=datetime.date.today() + datetime.timedelta(days=365),
        )

    def test_document_creation(self):
        """Pārbauda dokumenta izveidi un identifikatora ģenerēšanu."""
        self.assertEqual(QualityDocument.objects.count(), 1)
        self.assertIsNotNone(self.document.document_identifier)

    def test_document_string_representation(self):
        """Pārbauda __str__ metodi."""
        self.assertEqual(str(self.document), f"{self.document.document_identifier}: {self.document.title} (v{self.document.version})")


class ApprovalFlowTest(TestCase):
    """Testē dokumentu apstiprināšanas plūsmas funkcionalitāti."""

    @classmethod
    def setUpTestData(cls):
        cls.company = Company.objects.create(name="Test Company", identifier="TC")
        cls.doc_type = DocumentType.objects.create(name="Instrukcija", identifier="INST")
        cls.approver = User.objects.create_user(username="approver", password="password")
        cls.document = QualityDocument.objects.create(
            company=cls.company,
            document_type=cls.doc_type,
            title="Apstiprināmais dokuments",
            version="v01.01",
            review_date=datetime.date.today() + datetime.timedelta(days=180),
        )
        cls.approval = ApprovalFlow.objects.create(
            document=cls.document,
            approver=cls.approver,
            status="pending",
        )

    def test_approval_creation(self):
        """Pārbauda apstiprināšanas plūsmas izveidi."""
        self.assertEqual(ApprovalFlow.objects.count(), 1)
        self.assertEqual(self.approval.status, "pending")

    def test_approval_status_change(self):
        """Pārbauda statusa maiņu uz 'approved'."""
        self.approval.status = "approved"
        self.approval.save()
        self.assertEqual(self.approval.status, "approved")


class QualityDocumentFormTest(TestCase):
    """Testē QualityDocumentForm derīgumu."""

    @classmethod
    def setUpTestData(cls):
        cls.company = Company.objects.create(name="Test Company", identifier="TC")
        cls.doc_type = DocumentType.objects.create(name="Rīkojums", identifier="ORDER")
        cls.user = User.objects.create_user(username="formuser", password="password")

    def test_valid_form(self):
        """Pārbauda formu ar derīgiem datiem."""
        form_data = {
            "company": self.company.id,
            "document_type": self.doc_type.id,
            "title": "Formas tests",
            "version": "v01.02",
            "review_date": (datetime.date.today() + datetime.timedelta(days=90)).isoformat(),
        }
        form = QualityDocumentForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())

    def test_invalid_version_format(self):
        """Pārbauda formu ar nederīgu versijas formātu."""
        form_data = {
            "company": self.company.id,
            "document_type": self.doc_type.id,
            "title": "Nederīga versija",
            "version": "01.02",  # Trūkst 'v' sākumā
            "review_date": (datetime.date.today() + datetime.timedelta(days=90)).isoformat(),
        }
        form = QualityDocumentForm(data=form_data, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn("version", form.errors)


class DocumentViewsTest(TestCase):
    """Testē dokumentu skatus."""

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = User.objects.create_user(username="viewuser", password="password")
        cls.company = Company.objects.create(name="Test Company", identifier="TC")
        cls.doc_type = DocumentType.objects.create(name="Vadlīnijas", identifier="GUIDE")
        cls.document = QualityDocument.objects.create(
            company=cls.company,
            document_type=cls.doc_type,
            title="Skatu tests",
            version="v02.00",
            review_date=datetime.date.today() + datetime.timedelta(days=120),
        )

    def test_document_list_view_requires_login(self):
        """Pārbauda, vai dokumentu saraksts pieejams tikai autorizētiem lietotājiem."""
        response = self.client.get(reverse("quality_docs:document_list"))
        self.assertEqual(response.status_code, 302)  # Redirect uz pieteikšanās lapu

        self.client.login(username="viewuser", password="password")
        response = self.client.get(reverse("quality_docs:document_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Skatu tests")

    def test_document_detail_view(self):
        """Pārbauda dokumenta detalizēta skata pieejamību."""
        self.client.login(username="viewuser", password="password")
        response = self.client.get(reverse("quality_docs:document_detail", args=[self.document.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.document.title)
