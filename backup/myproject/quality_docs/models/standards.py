# quality_docs/models/standards.py
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey


class Standard(models.Model):
    """Quality standard model"""
    standard_number = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True,
        verbose_name=_("Standard Number")
    )
    # English fields
    title_en = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Title (English)"),
        help_text=_("Enter the standard title in English")
    )
    # Latvian fields
    title_lv = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Title (Latvian)"),
        help_text=_("Enter the standard title in Latvian")
    )
    version = models.CharField(
        max_length=20,
        verbose_name=_("Version")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated at")
    )

    class Meta:
        verbose_name = _("Standard")
        verbose_name_plural = _("Standards")
        ordering = ["standard_number"]

    def __str__(self):
        return f"{self.standard_number}: {self.version}"

    @property
    def title(self):
        """Get title in current language"""
        from django.utils.translation import get_language
        return self.title_en if get_language() == 'en' else self.title_lv

    def get_absolute_url(self):
        """Returns the URL for the standard detail view."""
        return reverse("quality_docs:standard-detail", kwargs={"pk": self.pk})


class StandardSection(MPTTModel):
    """Standard section with a hierarchical structure, entered in two languages."""
    standard = models.ForeignKey(
        "Standard",
        on_delete=models.CASCADE,
        related_name="sections",
        verbose_name=_("Standard"),
    )
    code = models.CharField(
        max_length=50,
        verbose_name=_("Section Code")
    )
    # Atrodam divus atsevišķus laucīšus standarta sadaļas nosaukumam
    title_en = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Section Title (English)"),
        help_text=_("Enter the section title in English")
    )
    title_lv = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Section Title (Latvian)"),
        help_text=_("Enter the section title in Latvian")
    )
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name=_("Parent")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated at")
    )

    class MPTTMeta:
        order_insertion_by = ["code"]

    class Meta:
        verbose_name = _("Standard Section")
        verbose_name_plural = _("Standard Sections")

    def __str__(self):
        # Atgriež kombinēto nosaukumu – abas valodas vērtības, ja pieejamas
        return f"{self.code}: {self.full_title}"

    @property
    def full_title(self):
        """Return both language titles side by side, e.g. 'English Title / Latvian Title'."""
        if self.title_en and self.title_lv:
            return f"{self.title_en} / {self.title_lv}"
        elif self.title_en:
            return self.title_en
        elif self.title_lv:
            return self.title_lv
        return ""

    @property
    def title(self):
        """Return title in current language."""
        from django.utils.translation import get_language
        return self.title_en if get_language() == 'en' else self.title_lv
