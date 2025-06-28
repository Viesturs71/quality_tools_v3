"""
Documents app models initialization.
"""
import importlib.util
from .document import Document
from .revision import DocumentRevision
from .section import DocumentSection
from .attachment import Attachment
from .section_document_link import SectionDocumentLink
# Add other model imports as needed
__all__ = [
    'Document',
    'DocumentRevision',
    'DocumentSection',
    'Attachment',
    'SectionDocumentLink',
]
# Import other models dynamically if needed
# Example:
# if importlib.util.find_spec("apps.documents.models.some_other_model"):
#     from .some_other_model import SomeOtherModel
#     __all__.append('SomeOtherModel')

