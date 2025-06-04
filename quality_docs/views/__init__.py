# quality_docs/views/__init__.py

# Import all views from the consolidated views.py file
from .views import (
    home,
    document_list,
    document_detail,
    document_create,
    document_update,
    document_delete,
    document_approve,
    document_sign,  # Add the new view function
    document_download,  # Add the new view
    approval_flow_create,
    approval_step_create,
    document_review_create,
    signature_request_create,
    document_distribution_create,
)

# Make sure all views are properly exposed at the package level
__all__ = [
    'home',
    'document_list',
    'document_detail',
    'document_create',
    'document_update',
    'document_delete',
    'document_approve',
    'document_sign',  # Add the new view function
    'document_download',  # Add the new view
    'approval_flow_create',
    'approval_step_create',
    'document_review_create',
    'signature_request_create',
    'document_distribution_create',
]

# Remove imports from non-existent modules
# Document views, workflow views, signature views, distribution views, and dashboard views 
# are now all consolidated in the views.py file
