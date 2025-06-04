from django import forms
from django.utils import timezone  # Add missing import
from django.utils.translation import gettext_lazy as _
from quality_docs.models.document import (
    DocumentType, DocumentCategory, DocumentSection, QualityDocument, DocumentAttachment,
    ApprovalFlow, ApprovalStep, DocumentReview, WorkflowRuleSet, WorkflowTemplate, WorkflowAssignment,
    SignatureRequest, DocumentDistribution
)

# ------------------ Base Forms ------------------
class BaseModelForm(forms.ModelForm):
    """Base form with common functionality."""
    class Meta:
        abstract = True

class PDFFileValidator(forms.FileField):
    """Validation for PDF file uploads."""
    def validate(self, value):
        super().validate(value)
        if not value.name.endswith('.pdf'):
            raise forms.ValidationError(_("Only PDF files are allowed."))

class DocumentUploadForm(BaseModelForm):
    """Base form for document uploads with PDF validation."""
    file = PDFFileValidator()

# ------------------ Document Forms ------------------
class DocumentTypeForm(BaseModelForm):
    class Meta:
        model = DocumentType
        fields = ['name', 'abbreviation', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'abbreviation': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class DocumentCategoryForm(BaseModelForm):
    class Meta:
        model = DocumentCategory
        fields = ['name', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class DocumentSectionForm(BaseModelForm):
    class Meta:
        model = DocumentSection
        fields = ['name', 'identifier']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'identifier': forms.TextInput(attrs={'class': 'form-control'}),
        }

class QualityDocumentForm(BaseModelForm):
    """Form for creating and updating QualityDocument."""
    class Meta:
        model = QualityDocument
        fields = [
            'title', 'document_number', 'document_type', 'section',
            'category', 'keywords', 'effective_date', 'expiry_date', 
            'review_date', 'is_template', 'file', 'uploaded_by'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter document title'}),
            'document_number': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'document_type': forms.Select(attrs={'class': 'form-select'}),
            'section': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'keywords': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter keywords'}),
            'effective_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'review_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_template': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'uploaded_by': forms.HiddenInput(),
        }

class DocumentApprovalForm(BaseModelForm):
    """Form for document approval process."""
    approval_comment = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False
    )
    
    class Meta:
        model = QualityDocument
        fields = ['is_approved', 'approval_comment']
        widgets = {
            'is_approved': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        if instance.is_approved:
            instance.approval_date = timezone.now()
            instance.approved_by = self.user
            instance.status = 'APPROVED'
            # Create approval record
            if hasattr(self, 'approval_comment') and self.cleaned_data.get('approval_comment'):
                ApprovalStep.objects.create(
                    approval_flow=instance.approval_flow,
                    comments=self.cleaned_data.get('approval_comment'),
                    is_complete=True,
                    approved=True,
                    approver=self.user,
                    completed_at=timezone.now()
                )
                
        if commit:
            instance.save()
        return instance

class DocumentSignatureForm(forms.Form):
    """
    Form for electronically signing a document.
    """
    confirmation = forms.BooleanField(
        required=True,
        label=_("I confirm that I have reviewed this document and approve its contents"),
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'})
    )
    
    comments = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-textarea'}),
        label=_("Optional comments")
    )

class DocumentAttachmentForm(BaseModelForm):
    class Meta:
        model = DocumentAttachment
        fields = ['document', 'file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

# ------------------ Workflow Forms ------------------
class WorkflowTemplateForm(BaseModelForm):
    class Meta:
        model = WorkflowTemplate
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

class WorkflowAssignmentForm(BaseModelForm):
    class Meta:
        model = WorkflowAssignment
        fields = ['workflow_template', 'document_type', 'document_category', 'document_section', 'rule_set', 'is_active', 'priority']
        widgets = {
            'workflow_template': forms.Select(attrs={'class': 'form-select'}),
            'document_type': forms.Select(attrs={'class': 'form-select'}),
            'document_category': forms.Select(attrs={'class': 'form-select'}),
            'document_section': forms.Select(attrs={'class': 'form-select'}),
            'rule_set': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'priority': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ApprovalFlowForm(BaseModelForm):
    class Meta:
        model = ApprovalFlow
        fields = ['document', 'name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ApprovalStepForm(BaseModelForm):
    class Meta:
        model = ApprovalStep
        fields = ['approval_flow', 'name', 'step_type', 'step_order', 'approver', 'is_required', 'is_complete', 'approved', 'comments']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'comments': forms.Textarea(attrs={'class': 'form-control'}),
        }

# ------------------ Review Forms ------------------
class DocumentReviewForm(BaseModelForm):
    class Meta:
        model = DocumentReview
        fields = ['document', 'reviewer', 'comments']
        widgets = {
            'comments': forms.Textarea(attrs={'class': 'form-control'}),
        }

# ------------------ Signature Forms ------------------
class SignatureRequestForm(BaseModelForm):
    class Meta:
        model = SignatureRequest
        fields = ['document', 'approval_step', 'signer', 'status', 'expiration_date', 'completed_date']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        # Ensure request_date is set if this is a new instance
        if not instance.pk and not instance.request_date:
            instance.request_date = timezone.now()
        if commit:
            instance.save()
        return instance

# ------------------ Distribution Forms ------------------
class DocumentDistributionForm(BaseModelForm):
    class Meta:
        model = DocumentDistribution
        fields = ['document']

class DocumentPublishForm(forms.Form):
    """Form to confirm document publication."""
    confirm = forms.BooleanField(
        required=True,
        label=_("I confirm this document should be published"),
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    def publish(self, document, user):
        document.status = 'PUBLISHED'
        document.published_at = timezone.now()
        document.published_by = user
        document.save()
        return document