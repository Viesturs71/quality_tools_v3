"""
Quality documents forms initialization.
"""
# Import all forms from the consolidated forms.py file
from .forms import (
    QualityDocumentForm,
    DocumentTypeForm,
    DocumentCategoryForm,
    DocumentSectionForm,
    ApprovalFlowForm,
    ApprovalStepForm,
    DocumentReviewForm,
    SignatureRequestForm,
    DocumentDistributionForm,
    DocumentApprovalForm,  # Ensure this is being imported
    DocumentSignatureForm,
    DocumentAttachmentForm,
    WorkflowTemplateForm,
    WorkflowAssignmentForm,
    PDFFileValidator,
    DocumentUploadForm,
)

# Make all forms available at the package level
__all__ = [
    'QualityDocumentForm',
    'DocumentTypeForm',
    'DocumentCategoryForm',
    'DocumentSectionForm',
    'ApprovalFlowForm',
    'ApprovalStepForm',
    'DocumentReviewForm',
    'SignatureRequestForm',
    'DocumentDistributionForm',
    'DocumentApprovalForm',  # Ensure this is in the __all__ list
    'DocumentSignatureForm',
    'DocumentAttachmentForm',
    'WorkflowTemplateForm',
    'WorkflowAssignmentForm',
    'PDFFileValidator',
    'DocumentUploadForm',
]
