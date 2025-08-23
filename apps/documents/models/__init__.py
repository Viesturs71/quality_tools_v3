"""
Documents app models initialization.
"""
from .document import Document
from .revision import DocumentRevision
from .section import DocumentSection
from .attachment import Attachment
from .section_document_link import SectionDocumentLink

__all__ = [
    'Document',
    'DocumentRevision',
    'DocumentSection',
    'Attachment',
    'SectionDocumentLink',
]

