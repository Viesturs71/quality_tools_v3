from django.db.models import Q
from django.db import DatabaseError
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Import the correct model - QualityDocument instead of Document
try:
    from quality_docs.models import QualityDocument

    def document_counts(request):
        """Context processor to add document counts to the global context."""
        if not request.user.is_authenticated:
            return {}

        try:
            # Izmantojam QualityDocument modeļa nosaukumu, nevis Document
            pending_count = QualityDocument.objects.filter(
                Q(status='review') | Q(status='pending')
            ).count()

            approved_count = QualityDocument.objects.filter(
                status='approved'
            ).count()

            return {
                'pending_document_count': pending_count,
                'approved_document_count': approved_count,
            }
        except DatabaseError:
            # Atgriežam 0, ja tabula vēl nav izveidota vai ir cita problēma
            return {
                'pending_document_count': 0,
                'approved_document_count': 0,
            }

except ImportError:
    # Ja modelis nav pieejams, izmantojam tukšu funkciju
    def document_counts(request):
        return {'pending_document_count': 0, 'approved_document_count': 0}


def navigation_modules(request):
    """
    Context processor to add navigation modules based on user permissions.
    """
    if not request.user.is_authenticated:
        return {'user_modules': []}

    modules = []

    # Documents module and submodules
    documents_submodules = []

    # My Documents - for all users
    documents_submodules.append({
        'name': _('My Documents'),
        'url_name': 'quality_docs:my_documents',
        'icon': 'fas fa-file-alt',
    })

    # Create Document - for all users
    documents_submodules.append({
        'name': _('Create Document'),
        'url_name': 'quality_docs:document_create',
        'icon': 'fas fa-plus',
    })

    # Document List - for all users
    documents_submodules.append({
        'name': _('All Documents'),
        'url_name': 'quality_docs:document_list',
        'icon': 'fas fa-list',
    })

    # Only add specialized views for users with specific permissions
    if request.user.has_perm('quality_docs.can_manage_approval_flow'):
        # Submitted Documents - for quality managers
        documents_submodules.append({
            'name': _('Submitted Documents'),
            'url_name': 'quality_docs:submitted_documents_list',
            'icon': 'fas fa-inbox',
            'badge': request.submitted_documents_count if hasattr(request, 'submitted_documents_count') else None,
        })

    if request.user.has_perm('quality_docs.can_approve_documents'):
        # Documents for Approval - for approvers
        documents_submodules.append({
            'name': _('Documents for Approval'),
            'url_name': 'quality_docs:documents_for_approval',
            'icon': 'fas fa-check-square',
        })

        # Approval Dashboard - for approvers
        documents_submodules.append({
            'name': _('Approval Dashboard'),
            'url_name': 'quality_docs:approval_dashboard',
            'icon': 'fas fa-tachometer-alt',
        })

    # Standards module - for users who can view standards
    if request.user.has_perm('quality_docs.view_standard'):
        documents_submodules.append({
            'name': _('Standards'),
            'url_name': 'quality_docs:standard_list',
            'icon': 'fas fa-book',
        })

    # Only add the Documents module if it has submodules
    if documents_submodules:
        modules.append({
            'name': _('Documents'),
            'icon': 'fas fa-folder',
            'submodules': documents_submodules
        })

    # Admin module - for staff users
    if request.user.is_staff:
        admin_submodules = [
            {
                'name': _('Administration'),
                'url_name': 'admin:index',
                'icon': 'fas fa-cogs',
            },
            # Removing problematic URL - auth_user_changelist
            # {
            #     'name': _('Users & Groups'),
#     'url_name': 'admin:auth_user_changelist',
#     'icon': 'fas fa-users',
# },
            {
                'name': _('Document Types'),
                'url_name': 'admin:quality_docs_documenttype_changelist',
                'icon': 'fas fa-tags',
            }
        ]

        modules.append({
            'name': _('Administration'),
            'icon': 'fas fa-user-shield',
            'submodules': admin_submodules
        })

    return {'user_modules': modules}
