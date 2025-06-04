#company/models.py
from django.db import models
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _


class Company(models.Model):
    """Company model representing an organization associated with users."""

    name = models.CharField(max_length=255, verbose_name=_("Company Name"))
    registration_number = models.CharField(
        max_length=20, unique=True, verbose_name=_("Registration Number")
    )
    address = models.TextField(blank=True, null=True, verbose_name=_("Address"))
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Phone"))
    email = models.EmailField(blank=True, null=True, verbose_name=_("Email"))
    website = models.URLField(blank=True, null=True, verbose_name=_("Website"))
    identifier = models.CharField(
        max_length=10,
        unique=True,
        editable=False,
        verbose_name=_("Company Identifier"),
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")

    def save(self, *args, **kwargs):
        """Saves the company and generates an identifier if not assigned."""
        if not self.identifier:
            self.identifier = self.generate_identifier()
        super().save(*args, **kwargs)

    def generate_identifier(self):
        """Generates a unique identifier based on the registration number."""
        base_id = self.registration_number[:3].upper()
        while True:
            random_suffix = get_random_string(length=3).upper()
            identifier = f"{base_id}-{random_suffix}"
            if not Company.objects.filter(identifier=identifier).exists():
                return identifier

    def get_absolute_url(self):
        """Returns the detail view URL for the company."""
        return reverse("company:detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name

class Department(models.Model):
    """
    Department model representing organizational units within a company.
    """
    name = models.CharField(max_length=255)
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='departments'
    )
    description = models.TextField(blank=True, null=True)
    manager = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"

    def __str__(self):
        return f"{self.name} ({self.company.name if self.company else 'No Company'})"
