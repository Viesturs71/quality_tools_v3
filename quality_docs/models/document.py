from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from company.models import Company

User = settings.AUTH_USER_MODEL

# ------------------ Document Types ------------------
class DocumentType(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name")
    abbreviation = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# ------------------ Document Categories ------------------
class DocumentCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# ------------------ Document Sections ------------------
class DocumentSection(models.Model):
    name = models.CharField(max_length=255)
    identifier = models.CharField(max_length=20)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.identifier} - {self.name}"

# ------------------ Quality Document ------------------
class QualityDocument(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', _('Draft')),
        ('REVIEW', _('Under Review')),
        ('APPROVED', _('Approved')),
        ('PUBLISHED', _('Published')),
        ('OBSOLETE', _('Obsolete')),
    ]
    
    title = models.CharField(max_length=255)
    document_number = models.CharField(max_length=100, unique=True)
    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE, verbose_name="Document Type")
    section = models.ForeignKey(DocumentSection, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(DocumentCategory, on_delete=models.SET_NULL, null=True, blank=True)
    file = models.FileField(upload_to='documents/')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    # Add status field
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='DRAFT')
    
    # Fix the company field reference to avoid the error
    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE,
        related_name='quality_documents',
        verbose_name=_("Company")
    )
    
    # Add missing fields
    keywords = models.CharField(max_length=255, blank=True, verbose_name="Keywords")
    effective_date = models.DateField(verbose_name="Effective Date", null=True, blank=True)
    expiry_date = models.DateField(verbose_name="Expiry Date", null=True, blank=True)
    review_date = models.DateField(verbose_name="Review Date", null=True, blank=True)
    is_template = models.BooleanField(default=False, verbose_name="Is Template")
    
    # Add approval and signature fields
    is_approved = models.BooleanField(default=False, verbose_name="Is Approved")
    approval_date = models.DateTimeField(null=True, blank=True, verbose_name="Approval Date")
    approved_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='quality_approved_documents',  # Changed from 'approved_documents'
        verbose_name="Approved By"
    )
    electronic_signature = models.BooleanField(default=False, verbose_name="Electronically Signed")
    signature_date = models.DateTimeField(null=True, blank=True, verbose_name="Signature Date")
    
    # Publication tracking
    published_at = models.DateTimeField(null=True, blank=True, verbose_name="Published At")
    published_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='quality_published_documents',
        verbose_name="Published By",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.document_number} - {self.title}"

    def generate_document_number(self):
        """Generate a document number using company identifier and sequential numbering."""
        company_identifier = self.company.identifier
        doc_type_code = self.document_type.abbreviation if self.document_type else "DOC"
        sequence = QualityDocument.objects.filter(company=self.company).count() + 1
        
        return f"{company_identifier}-{doc_type_code}-{sequence:04d}"
    
    def save(self, *args, **kwargs):
        if not self.document_number:
            self.document_number = self.generate_document_number()
        super().save(*args, **kwargs)

# ------------------ Approval Flow ------------------
class ApprovalFlow(models.Model):
    document = models.OneToOneField(QualityDocument, on_delete=models.CASCADE, related_name='approval_flow')
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Approval Flow for {self.document.title}"

# ------------------ Approval Step ------------------
class ApprovalStep(models.Model):
    STEP_TYPES = [
        ('REVIEW', _('Review')),
        ('APPROVAL', _('Approval')),
    ]

    approval_flow = models.ForeignKey(ApprovalFlow, on_delete=models.CASCADE, related_name='steps')
    name = models.CharField(max_length=255)
    step_type = models.CharField(max_length=10, choices=STEP_TYPES)
    step_order = models.PositiveIntegerField()
    approver = models.ForeignKey(User, on_delete=models.CASCADE)
    is_required = models.BooleanField(default=True)
    is_complete = models.BooleanField(default=False)
    approved = models.BooleanField(null=True)
    comments = models.TextField(blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def complete_step(self, approved):
        self.is_complete = True
        self.approved = approved
        self.completed_at = timezone.now()
        self.save()

    def __str__(self):
        return f"Step {self.step_order} - {self.name}"

# ------------------ Document Review ------------------
class DocumentReview(models.Model):
    document = models.ForeignKey(QualityDocument, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    comments = models.TextField(blank=True)
    reviewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.reviewer} on {self.document.title}"

# ------------------ Document Attachment ------------------
class DocumentAttachment(models.Model):
    document = models.ForeignKey(QualityDocument, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

# ------------------ Workflow Models ------------------
class WorkflowRuleSet(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    auto_progress = models.BooleanField(default=True)
    require_all_approvals = models.BooleanField(default=True)
    allow_parallel_review = models.BooleanField(default=False)
    notify_on_rejection = models.BooleanField(default=True)
    auto_publish_on_completion = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class WorkflowTemplate(models.Model):
    """Model representing a workflow template that can be assigned to documents."""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class WorkflowAssignment(models.Model):
    workflow_template = models.ForeignKey('WorkflowTemplate', on_delete=models.CASCADE)
    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE, null=True, blank=True)
    document_category = models.ForeignKey(DocumentCategory, on_delete=models.CASCADE, null=True, blank=True)
    document_section = models.ForeignKey(DocumentSection, on_delete=models.CASCADE, null=True, blank=True)
    rule_set = models.ForeignKey(WorkflowRuleSet, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    priority = models.PositiveIntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-priority']

class WorkflowNotification(models.Model):
    NOTIFICATION_TYPES = [
        ('WORKFLOW_STARTED', _('Workflow Started')),
        ('STEP_ASSIGNED', _('Step Assigned')),
        ('STEP_COMPLETED', _('Step Completed')),
        ('DOCUMENT_APPROVED', _('Document Approved')),
        ('DOCUMENT_REJECTED', _('Document Rejected')),
        ('WORKFLOW_COMPLETED', _('Workflow Completed')),
    ]
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES)
    document = models.ForeignKey(QualityDocument, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class SignatureRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', _('Pending')),
        ('COMPLETED', _('Completed')),
        ('REJECTED', _('Rejected')),
    ]
    document = models.ForeignKey(QualityDocument, on_delete=models.CASCADE)
    approval_step = models.ForeignKey(ApprovalStep, on_delete=models.CASCADE)
    signer = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    request_date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField()
    completed_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Signature request for {self.document}"

class DocumentDistribution(models.Model):
    """
    Document Distribution model - represents document distribution to users.
    """
    document = models.ForeignKey(QualityDocument, on_delete=models.CASCADE, related_name='distributions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    distribution_date = models.DateTimeField(auto_now_add=True)
    action_type = models.CharField(max_length=20, default='DISTRIBUTION')
    action_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        app_label = 'quality_docs'
        verbose_name = _('Document Distribution')
        verbose_name_plural = _('Document Distributions')
        
    def __str__(self):
        return f"Distribution of {self.document} to {self.user}"

class DocumentAcknowledgment(models.Model):
    """
    Document Acknowledgment model - represents user acknowledgment of document receipt.
    """
    document = models.ForeignKey(QualityDocument, on_delete=models.CASCADE, related_name='acknowledgments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    acknowledged_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        app_label = 'quality_docs'
        verbose_name = _('Document Acknowledgment')
        verbose_name_plural = _('Document Acknowledgments')
        
    def __str__(self):
        return f"Acknowledgment of {self.document} by {self.user}"

# ------------------ Document Model ------------------
class Document(models.Model):
    """Model representing a document."""
    title = models.CharField(max_length=255, verbose_name="Title")
    document_number = models.CharField(max_length=50, unique=True, verbose_name="Document Number")
    version = models.CharField(max_length=20, verbose_name="Version")
    document_type = models.ForeignKey('DocumentType', on_delete=models.CASCADE, verbose_name="Document Type")
    is_template = models.BooleanField(default=False, verbose_name="Is Template")
    keywords = models.CharField(max_length=255, verbose_name="Keywords", blank=True)
    effective_date = models.DateField(verbose_name="Effective Date", null=True, blank=True)
    expiry_date = models.DateField(verbose_name="Expiry Date", null=True, blank=True)
    review_date = models.DateField(verbose_name="Review Date", null=True, blank=True)
    owner = models.CharField(max_length=255, verbose_name="Owner")
    department = models.CharField(max_length=255, verbose_name="Department")
    file = models.FileField(upload_to='documents/', verbose_name="File")
    
    # Add electronic document management fields
    is_approved = models.BooleanField(default=False, verbose_name="Is Approved")
    approval_date = models.DateTimeField(null=True, blank=True, verbose_name="Approval Date")
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True, 
        related_name='standard_approved_documents',  # Changed from 'approved_documents'
        verbose_name="Approved By"
    )
    electronic_signature = models.BooleanField(default=False, verbose_name="Electronically Signed")
    signature_date = models.DateTimeField(null=True, blank=True, verbose_name="Signature Date")
    revision_history = models.TextField(blank=True, verbose_name="Revision History")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return self.title
        
    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"
        ordering = ['-updated_at']
        permissions = [
            ("view_all_documents", "Can view all documents regardless of department"),
            ("approve_documents", "Can approve documents"),
            ("sign_documents", "Can electronically sign documents"),
        ]
    
    def save(self, *args, **kwargs):
        # Auto-generate document number if not provided
        if not self.pk and not self.document_number:
            last_doc = Document.objects.order_by('-id').first()
            last_id = last_doc.id if last_doc else 0
            self.document_number = f"DOC-{self.document_type.abbreviation}-{last_id + 1:04d}"
        super().save(*args, **kwargs)