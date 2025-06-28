from django.db import models
from django.utils.translation import gettext_lazy as _
from .document import Document
from .section import DocumentSection


class SectionDocumentLink(models.Model):
    """Link between document sections and documents for traceability."""
    section = models.ForeignKey(
        DocumentSection,
        on_delete=models.CASCADE,
        related_name='document_links',
        verbose_name=_("Section")
    )
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name='section_links',
        verbose_name=_("Document")
    )
    description = models.TextField(_("Link Description"), blank=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Section Document Link")
        verbose_name_plural = _("Section Document Links")
        unique_together = ('section', 'document')
        ordering = ('section', 'document')

    def __str__(self):
        return f"{self.section.name} → {self.document.title}"
