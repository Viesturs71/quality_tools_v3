# company/forms.py
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Company  # Updated import path to use relative import


class CompanyForm(forms.ModelForm):
    """Form for creating and editing a company."""

    class Meta:
        model = Company
        fields = [
            "name",
            "registration_number",
            "address",
            "phone",
            "email",
            "is_active",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": _("Company Name")}),
            "registration_number": forms.TextInput(attrs={"class": "form-control", "placeholder": _("Registration Number")}),
            "address": forms.TextInput(attrs={"class": "form-control", "placeholder": _("Address")}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": _("Phone")}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": _("Email Address")}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_registration_number(self):
        """Checks if the registration number is unique."""
        registration_number = self.cleaned_data.get("registration_number")
        if Company.objects.filter(registration_number=registration_number).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(_("A company with this registration number already exists."))
        return registration_number
