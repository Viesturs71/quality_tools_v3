from django.db import models
from .document import Document
from django.utils.translation import gettext_lazy as _


class DocumentRevision(models.Model):
    document    = models.ForeignKey(Document, on_delete=models.CASCADE)
    revision_number = models.CharField(max_length=20, verbose_name=_("Revision Number"))
    revision_date = models.DateField(verbose_name=_("Revision Date"))
    description = models.TextField(verbose_name=_("Description"))
    is_current = models.BooleanField(default=False, verbose_name=_("Current Revision"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Document Revision")
        verbose_name_plural = _("Document Revisions")
        ordering = ["-revision_date"]

    def __str__(self):
        return self.revision_number
