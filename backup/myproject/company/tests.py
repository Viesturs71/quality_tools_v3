#company/tests.py
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from company.models import Company
from company.serializers import CompanySerializer


class CompanyModelTest(TestCase):
    """Testē Company modeļa funkcionalitāti."""

    def setUp(self):
        self.company = Company.objects.create(
            name="Test Uzņēmums",
            registration_number="123456789",
            address="Testa iela 1, Rīga",
            phone="29123456",
            email="test@company.com",
            is_active=True
        )

    def test_company_creation(self):
        """Pārbauda, vai uzņēmums tiek veiksmīgi izveidots."""
        self.assertEqual(Company.objects.count(), 1)
        self.assertEqual(self.company.name, "Test Uzņēmums")

    def test_company_str(self):
        """Pārbauda __str__ metodi."""
        self.assertEqual(str(self.company), f"{self.company.name} ({self.company.identifier})")


class CompanySerializerTest(TestCase):
    """Testē Company sērijizatoru."""

    def setUp(self):
        self.company_data = {
            "name": "Jauns Uzņēmums",
            "registration_number": "987654321",
            "address": "Brīvības iela 10, Rīga",
            "phone": "29123456",
            "email": "jauns@company.com",
            "is_active": True
        }

    def test_valid_serializer(self):
        """Pārbauda sērijizatoru ar derīgiem datiem."""
        serializer = CompanySerializer(data=self.company_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_registration_number(self):
        """Pārbauda reģistrācijas numura unikālitāti."""
        Company.objects.create(**self.company_data)
        serializer = CompanySerializer(data=self.company_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("registration_number", serializer.errors)


class CompanyAPITest(TestCase):
    """Testē Company API galvenās darbības."""

    def setUp(self):
        self.client = APIClient()
        self.company = Company.objects.create(
            name="API Uzņēmums",
            registration_number="555555555",
            address="API iela 5, Rīga",
            phone="29999999",
            email="api@company.com",
            is_active=True
        )
        self.list_url = reverse("company-list")
        self.detail_url = reverse("company-detail", kwargs={"pk": self.company.pk})

    def test_get_company_list(self):
        """Pārbauda uzņēmumu saraksta iegūšanu."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_get_company_detail(self):
        """Pārbauda konkrēta uzņēmuma datu iegūšanu."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.company.name)

    def test_create_company_unauthenticated(self):
        """Pārbauda, ka neautorizēts lietotājs nevar izveidot uzņēmumu."""
        response = self.client.post(self.list_url, {
            "name": "Jauns API Uzņēmums",
            "registration_number": "333333333",
            "address": "Jaunā iela 2, Rīga",
            "phone": "28888888",
            "email": "new@company.com",
            "is_active": True
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
