"""
This module re-exports all models from the models package.
"""
from .models.document import Document
from .models.attachment import DocumentAttachment
from .models.revision import DocumentRevision
from .models.section import DocumentSection
from .models.category import Category
from .models.comment import DocumentComment

# For backward compatibility
__all__ = [
    'Document',

    'DocumentAttachment',
    'DocumentRevision',
    'DocumentSection',
    'Category',
    'DocumentComment',
]
