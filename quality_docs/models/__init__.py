"""
Quality documents models initialization.
This file provides backward compatibility for existing imports.
"""
# Import all models directly from document.py since all models are defined there
from .document import (
    DocumentType, 
    QualityDocument, 
    Document, 
    DocumentSection, 
    DocumentCategory,
    DocumentAttachment,
    DocumentReview,
    ApprovalFlow,
    ApprovalStep,
    WorkflowRuleSet,
    WorkflowTemplate,
    WorkflowAssignment,
    WorkflowNotification,
    SignatureRequest,
    DocumentDistribution,
    DocumentAcknowledgment
)

# Create module aliases for backward compatibility with existing imports
import sys
import types

# Create a documents module alias
documents_module = types.ModuleType('quality_docs.models.documents')
for model_name in [
    'DocumentType', 'QualityDocument', 'Document', 'DocumentSection', 'DocumentCategory'
]:
    if model_name in globals():
        setattr(documents_module, model_name, globals()[model_name])
sys.modules['quality_docs.models.documents'] = documents_module

# Create a standards module alias
standards_module = types.ModuleType('quality_docs.models.standards')
# Standard and StandardSection might be imported from elsewhere
# Let's create placeholder classes to avoid errors
class Standard:
    pass
    
class StandardSection:
    pass
    
standards_module.Standard = Standard
standards_module.StandardSection = StandardSection
sys.modules['quality_docs.models.standards'] = standards_module

# Define all exported models
__all__ = [
    'DocumentType',
    'QualityDocument', 
    'Document', 
    'DocumentSection', 
    'DocumentCategory',
    'DocumentAttachment',
    'DocumentReview',
    'ApprovalFlow',
    'ApprovalStep',
    'WorkflowRuleSet',
    'WorkflowTemplate',
    'WorkflowAssignment',
    'WorkflowNotification',
    'SignatureRequest',
    'DocumentDistribution',
    'DocumentAcknowledgment'
]
