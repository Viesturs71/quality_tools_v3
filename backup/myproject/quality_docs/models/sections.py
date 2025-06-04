#quality_docs/models/sections.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey


class DocumentSection(MPTTModel):
    identifier = models.CharField(max_length=10, verbose_name=_("Identifier"))
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name=_("Parent Section")
    )

    class MPTTMeta:
        order_insertion_by = ['identifier']

    class Meta:
        ordering = ['identifier']  # <- Šis nodrošina kārtošanu admin panelī
        verbose_name = _("Document Section")
        verbose_name_plural = _("Document Sections")

    def __str__(self):
        return f"{self.identifier} - {self.title}"

    def clean(self):
        # Validation removed to allow sections to exist independently without a document
        pass

