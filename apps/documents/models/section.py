from django.db import models
from django.utils.translation import gettext_lazy as _


class DocumentSection(models.Model):
    """
    Section within a document
    """
    document = models.ForeignKey('Document', on_delete=models.CASCADE, related_name='sections', verbose_name='Dokuments')
    section_number = models.CharField(max_length=50, verbose_name=_("Section Number"))
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    content = models.TextField(blank=True, verbose_name=_("Content"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))
    order = models.PositiveIntegerField(default=1, verbose_name='Secība')
    
    class Meta:
        verbose_name = 'Dokumenta sadaļa'
        verbose_name_plural = 'Dokumenta sadaļas'
        ordering = ['document', 'order']
        unique_together = ['document', 'order']
    
    def __str__(self):
        return f"{self.document.document_number} - {self.title}"
