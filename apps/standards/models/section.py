from django.db import models
from django.utils.translation import gettext_lazy as _


class StandardSection(models.Model):
    title = models.CharField(_('Title'), max_length=255)
    description = models.TextField(_('Description'), blank=True, null=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='subsections',
        blank=True,
        null=True,
        verbose_name=_('Parent Section')
    )

    class Meta:
        verbose_name = _('Standard Section')
        verbose_name_plural = _('Standard Sections')

    def __str__(self):
        return self.title
class StandardSubsection(models.Model):
    section = models.ForeignKey(StandardSection, on_delete=models.CASCADE, related_name="subsections_new", verbose_name="Section")
    subsection_number = models.CharField(max_length=20, verbose_name="Subsection Number")
    title = models.CharField(max_length=255, verbose_name="Subsection Title")
    content = models.TextField(blank=True, verbose_name="Content")
    order = models.PositiveIntegerField(default=0, verbose_name="Order")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Standard Subsection"
        verbose_name_plural = "Standard Subsections"
        ordering = ["section", "order", "subsection_number"]

    def __str__(self):
        return self.subsection_number
