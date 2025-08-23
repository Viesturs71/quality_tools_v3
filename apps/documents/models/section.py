from django.db import models
from django.utils.translation import gettext_lazy as _


class DocumentSection(models.Model):
    """
    A section of a document representing a distinct part of the document content.
    """
    document = models.ForeignKey(
        'documents.Document',
        on_delete=models.CASCADE,
        related_name='sections',
        verbose_name=_('Document'),
        null=True,
        blank=True,
        default=None  # <-- add default=None to allow saving without document
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subsections',
        verbose_name=_('Parent Section')
    )
    code = models.CharField(_('Section number'), max_length=50)
    # Require both original and alternative language fields (no blank=True)
    title_original = models.CharField(_('Section title (original)'), max_length=200)
    title_alt = models.CharField(_('Section title (alternative)'), max_length=200)
    content_original = models.TextField(_('Content (original)'))
    content_alt = models.TextField(_('Content (alternative)'))
    order = models.PositiveIntegerField(_('Order'), default=0)

    class Meta:
        verbose_name = _('Document Section')
        verbose_name_plural = _('Document Sections')
        ordering = ['document', 'parent__id', 'order']
        constraints = [
            models.UniqueConstraint(fields=['document', 'code'], name='unique_document_code')
        ]

    def __str__(self):
        # Show both titles if available
        return f"{self.code} - {self.title_original}" + (f" / {self.title_alt}" if self.title_alt else "")

    def get_title(self, use_alt=False):
        return self.title_alt if use_alt else self.title_original

    def get_content(self, use_alt=False):
        return self.content_alt if use_alt else self.content_original

    def get_full_code(self):
        if self.parent:
            return f"{self.parent.get_full_code()}.{self.code}"
        return self.code

    def get_full_title(self, use_alt=False):
        if self.parent:
            return f"{self.parent.get_full_title(use_alt)} / {self.get_title(use_alt)}"
        return self.get_title(use_alt)
