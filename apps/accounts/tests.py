"""
accounts/tests.py
Reģistrācijas un profila skatu testēšana.
"""

import pytest
pytest.importorskip("django")

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class RegisterViewTests(TestCase):
    """Testē reģistrācijas skatu un tā funkcionalitāti."""

    def setUp(self):
        self.register_url = reverse("accounts:register")
        self.login_url = reverse("accounts:login")
        self.profile_url = reverse("accounts:user_profile")
        self.user_credentials = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "Testpassword123",
            "password2": "Testpassword123",
        }

    def test_register_view_status_code(self):
        """Pārbauda, vai reģistrācijas lapa ir pieejama (statuss 200)."""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)

    def test_register_user_success(self):
        """Pārbauda veiksmīgu lietotāja reģistrāciju un pāradresāciju uz login."""
        response = self.client.post(self.register_url, self.user_credentials)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_register_user_password_mismatch(self):
        """Pārbauda, vai reģistrācija neizdodas, ja paroles nesakrīt."""
        self.user_credentials["password2"] = "WrongPassword123"
        response = self.client.post(self.register_url, self.user_credentials)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, "form", "password2", "The two password fields didn’t match.")
        self.assertFalse(User.objects.filter(username="testuser").exists())

    def test_register_user_existing_username(self):
        """Pārbauda reģistrācijas kļūdu ar jau esošu lietotājvārdu."""
        User.objects.create_user(username="testuser", email="existing@example.com", password="Testpassword123")
        response = self.client.post(self.register_url, self.user_credentials)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, "form", "username", "A user with that username already exists.")

    def test_profile_access_requires_login(self):
        """Pārbauda, vai profila lapa nav pieejama bez autorizācijas."""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{self.login_url}?next={self.profile_url}")

    def test_profile_access_with_login(self):
        """Pārbauda, vai autorizēts lietotājs var piekļūt profilam."""
        User.objects.create_user(username="testuser", password="Testpassword123")
        self.client.login(username="testuser", password="Testpassword123")
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
