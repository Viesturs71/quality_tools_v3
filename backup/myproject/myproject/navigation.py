from django.utils.translation import gettext_lazy as _


def user_modules(request):
    return {
        'user_modules': [
            {
                'name': _('User Panel'),
                'icon': 'fas fa-user',
                'submodules': [
                    {'name': _('Admin'), 'url_name': 'admin:index', 'icon': 'fas fa-cog'},
                    {'name': _('User Profile'), 'url_name': 'users:profile', 'icon': 'fas fa-id-badge'},
                    {'name': _('Activity Log'), 'url_name': 'users:activity_log', 'icon': 'fas fa-clipboard-list'},
                    {'name': _('Logout'), 'url_name': 'logout', 'icon': 'fas fa-sign-out-alt'},
                ]
            },
            {
                'name': _('Document Management'),
                'icon': 'fas fa-folder',
                'submodules': [
                    {'name': _('Documents List'), 'url_name': 'quality_docs:document_list', 'icon': 'fas fa-list'},
                    {'name': _('Create Document'), 'url_name': 'quality_docs:document_create', 'icon': 'fas fa-plus'},
                    {'name': _('Documents for Reconciliation'), 'url_name': 'quality_docs:documents_for_reconciliation', 'icon': 'fas fa-sync'},
                    {'name': _('Documents for Approval'), 'url_name': 'quality_docs:documents_for_approval', 'icon': 'fas fa-check-double'},
                ]
            },
            {
                'name': _('Standards'),
                'icon': 'fas fa-book',
                'submodules': [
                    {'name': _('Standards List'), 'url_name': 'quality_docs:standard_list', 'icon': 'fas fa-list'},
                ]
            },
            {
                'name': _('Equipment'),
                'icon': 'fas fa-cogs',
                'submodules': [
                    {'name': _('Equipment Registry'), 'url_name': 'equipment:equipment_list', 'icon': 'fas fa-tools'},
                ]
            },
            {
                'name': _('Personnel'),
                'icon': 'fas fa-users',
                'submodules': [
                    {'name': _('Personnel Registry'), 'url_name': 'personnel:personnel_list', 'icon': 'fas fa-id-card'},
                ]
            },
            {
                'name': _('Audits'),
                'icon': 'fas fa-clipboard-check',
                'submodules': [
                    {'name': _('Audit List'), 'url_name': 'audits:audit_list', 'icon': 'fas fa-clipboard-list'},
                ]
            },
        ]
    }
