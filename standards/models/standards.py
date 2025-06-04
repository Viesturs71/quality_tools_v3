"""
Standards models definition.
All standard-related models are defined in this file.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

class Standard(models.Model):
    """
    Standard model - represents a standard document.
    """
    number = models.CharField(max_length=50, unique=True, verbose_name=_("Standard Number"))
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    title_en = models.CharField(max_length=255, blank=True, verbose_name=_("Title in English"))
    publication_year = models.IntegerField(verbose_name=_("Publication Year"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))
    
    class Meta:
        app_label = 'standards'
        verbose_name = _("Standard")
        verbose_name_plural = _("Standards")
        ordering = ["number"]
    
    def __str__(self):
        return f"{self.number} - {self.title}"

class StandardSection(MPTTModel):
    """
    Standard section model - represents a section within a standard.
    """
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE, related_name="sections", verbose_name=_("Standard"))
    name = models.CharField(max_length=255, verbose_name=_("Section Name"))
    code = models.CharField(max_length=20, blank=True, verbose_name=_("Section Code"))
    content = models.TextField(blank=True, verbose_name=_("Content"))
    content_en = models.TextField(blank=True, verbose_name=_("Content in English"))
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name=_("Parent Section"))
    order = models.PositiveIntegerField(default=0, verbose_name=_("Order"))
    
    class MPTTMeta:
        order_insertion_by = ['order']
    
    class Meta:
        app_label = 'standards'
        verbose_name = _("Standard Section")
        verbose_name_plural = _("Standard Sections")
        unique_together = ('standard', 'code')
    
    def __str__(self):
        return f"{self.standard.number} - {self.name}"

class StandardSubsection(models.Model):
    """
    Standard subsection model - represents a subsection within a standard section.
    """
    section = models.ForeignKey(StandardSection, on_delete=models.CASCADE, related_name="subsections", verbose_name=_("Section"))
    number = models.CharField(max_length=20, verbose_name=_("Subsection Number"))
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    title_en = models.CharField(max_length=255, blank=True, verbose_name=_("Title in English"))
    content = models.TextField(blank=True, verbose_name=_("Content"))
    content_en = models.TextField(blank=True, verbose_name=_("Content in English"))
    order = models.PositiveIntegerField(default=0, verbose_name=_("Order"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))
    
    class Meta:
        app_label = 'standards'
        verbose_name = _("Standard Subsection")
        verbose_name_plural = _("Standard Subsections")
        ordering = ["order"]
        unique_together = ('section', 'number')
    
    def __str__(self):
        return f"{self.section.standard.number} - {self.section.name} - {self.number}"

class StandardRequirement(models.Model):
    """
    Standard requirement model - represents specific requirements within standards.
    """
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE, related_name="requirements", verbose_name=_("Standard"))
    section = models.ForeignKey(StandardSection, on_delete=models.CASCADE, related_name="requirements", verbose_name=_("Section"), null=True, blank=True)
    subsection = models.ForeignKey(StandardSubsection, on_delete=models.CASCADE, related_name="requirements", verbose_name=_("Subsection"), null=True, blank=True)
    requirement_id = models.CharField(max_length=50, verbose_name=_("Requirement ID"))
    description = models.TextField(verbose_name=_("Description"))
    description_en = models.TextField(blank=True, verbose_name=_("Description in English"))
    is_mandatory = models.BooleanField(default=True, verbose_name=_("Is Mandatory"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))
    
    class Meta:
        app_label = 'standards'
        verbose_name = _("Standard Requirement")
        verbose_name_plural = _("Standard Requirements")
        ordering = ["requirement_id"]
    
    def __str__(self):
        return f"{self.standard.number} - {self.requirement_id}"

class StandardAttachment(models.Model):
    """
    Standard attachment model - for files attached to standards.
    """
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE, related_name="attachments", verbose_name=_("Standard"))
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    file = models.FileField(upload_to='standards/', verbose_name=_("File"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    
    class Meta:
        app_label = 'standards'
        verbose_name = _("Standard Attachment")
        verbose_name_plural = _("Standard Attachments")
    
    def __str__(self):
        return f"{self.standard.number} - {self.name}"

class StandardRevision(models.Model):
    """
    Standard revision model - tracks changes to standards.
    """
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE, related_name="revisions", verbose_name=_("Standard"))
    revision_number = models.CharField(max_length=20, verbose_name=_("Revision Number"))
    revision_date = models.DateField(verbose_name=_("Revision Date"))
    description = models.TextField(verbose_name=_("Description of Changes"))
    is_major = models.BooleanField(default=False, verbose_name=_("Major Revision"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    
    class Meta:
        app_label = 'standards'
        verbose_name = _("Standard Revision")
        verbose_name_plural = _("Standard Revisions")
        ordering = ["-revision_date"]
    
    def __str__(self):
        return f"{self.standard.number} - Revision {self.revision_number}"

class StandardComplianceStatus(models.Model):
    """
    Standard compliance status model - tracks compliance with standards.
    """
    STATUS_CHOICES = [
        ('COMPLIANT', _('Compliant')),
        ('PARTIALLY', _('Partially Compliant')),
        ('NON_COMPLIANT', _('Non-Compliant')),
        ('NOT_APPLICABLE', _('Not Applicable')),
        ('UNDER_REVIEW', _('Under Review')),
    ]
    
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE, related_name="compliance_statuses", verbose_name=_("Standard"))
    requirement = models.ForeignKey(StandardRequirement, on_delete=models.CASCADE, related_name="compliance_statuses", verbose_name=_("Requirement"), null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='UNDER_REVIEW', verbose_name=_("Status"))
    evidence = models.TextField(blank=True, verbose_name=_("Compliance Evidence"))
    notes = models.TextField(blank=True, verbose_name=_("Notes"))
    assessed_date = models.DateField(verbose_name=_("Assessment Date"), null=True, blank=True)
    next_review_date = models.DateField(verbose_name=_("Next Review Date"), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))
    
    class Meta:
        app_label = 'standards'
        verbose_name = _("Standard Compliance Status")
        verbose_name_plural = _("Standard Compliance Statuses")
        ordering = ["-assessed_date"]
    
    def __str__(self):
        return f"{self.standard.number} - {self.status}"

class StandardDocument(models.Model):
    """
    Standard document model - represents documents related to standards.
    """
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE, related_name="documents", verbose_name=_("Standard"))
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    document_type = models.CharField(max_length=50, verbose_name=_("Document Type"))
    file = models.FileField(upload_to='standards/documents/', verbose_name=_("Document File"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    version = models.CharField(max_length=20, blank=True, verbose_name=_("Version"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))
    
    class Meta:
        app_label = 'standards'
        verbose_name = _("Standard Document")
        verbose_name_plural = _("Standard Documents")
    
    def __str__(self):
        return f"{self.standard.number} - {self.title}"
