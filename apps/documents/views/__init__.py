"""
Documents app views initialization.
"""
from .document_views import (
    DocumentListView,
    DocumentDetailView,
    DocumentCreateView,
    DocumentUpdateView,
    DocumentDeleteView,
    register_document,
    user_documents
)

__all__ = [
    'DocumentListView',
    'DocumentDetailView',
    'DocumentCreateView',
    'DocumentUpdateView',
    'DocumentDeleteView',
    'register_document',
    'user_documents'
]
