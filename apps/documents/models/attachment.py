from django.db import models
from django.utils.translation import gettext_lazy as _


class DocumentAttachment(models.Model):
    """
    File attachment for a document
    """
    document = models.ForeignKey('Document', on_delete=models.CASCADE, related_name='attachments', verbose_name='Dokuments')
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    file = models.FileField(upload_to="documents/attachments/", verbose_name=_("File"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Document Attachment")
        verbose_name_plural = _("Document Attachments")
        ordering = ["title"]

    def __str__(self):
        return self.title
