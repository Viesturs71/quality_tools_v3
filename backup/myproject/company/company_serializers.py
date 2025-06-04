### 📄 company_serializers.py**
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from company.models import Company


class CompanySerializer(serializers.ModelSerializer):
    """Company serializer with additional validations."""

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)

    class Meta:
        model = Company
        fields = [
            "id",
            "name",
            "registration_number",
            "identifier",
            "address",
            "phone",
            "email",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("identifier", "created_at", "updated_at")

    def validate_registration_number(self, value):
        """Checks if the registration number is unique."""
        if self.instance:
            if Company.objects.exclude(pk=self.instance.pk).filter(registration_number=value).exists():
                raise serializers.ValidationError(_("A company with this registration number already exists."))
        else:
            if Company.objects.filter(registration_number=value).exists():
                raise serializers.ValidationError(_("A company with this registration number already exists."))
        return value

    def validate_email(self, value):
        """Additional email format validation (optional but recommended)."""
        if value and not serializers.EmailField().run_validation(value):
            raise serializers.ValidationError(_("Invalid email format."))
        return value
