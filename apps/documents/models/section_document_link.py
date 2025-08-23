from django.db import models
from django.utils.translation import gettext_lazy as _

class SectionDocumentLink(models.Model):
    """Link between document sections and documents for traceability."""
    section = models.ForeignKey(
        'documents.DocumentSection',
        on_delete=models.CASCADE,
        related_name='document_links',
        verbose_name=_("Section")
    )
    document = models.ForeignKey(
        'documents.Document',
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
        ordering = ('section', 'document')
        constraints = [
            models.UniqueConstraint(fields=['section', 'document'], name='unique_section_document_link')
        ]

    def __str__(self):
        # Pielāgo pēc modeļa lauku nosaukumiem!
        return f"{self.section.code} → {self.document.original_title}"