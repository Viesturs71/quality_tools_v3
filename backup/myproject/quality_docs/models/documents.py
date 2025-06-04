"""
DEPRECATED: This file has been reorganized.
Models are now located in separate files:
- DocumentType: document_type.py
- QualityDocument: document.py
- DocumentSection: document_section.py
- DocumentReview: document_review.py

Import from quality_docs.models instead.
"""

# Redirect imports to maintain backward compatibility temporarily
from .document_type import DocumentType
from .document import QualityDocument
from .document_section import DocumentSection
from .document_review import DocumentReview

__all__ = [
    'DocumentType',
    'QualityDocument', 
    'DocumentSection',
    'DocumentReview',
]

def document_file_path(instance, filename):
    # define the upload path for document files
    return f"quality_docs/documents/{instance.id}/{filename}"
