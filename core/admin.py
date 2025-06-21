from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.conf import settings

# Set admin site attributes
admin.site.site_header = _("Quality Tools Administration")
admin.site.site_title = _("Quality Tools Admin")
admin.site.index_title = _("Dashboard")

class CustomAdminSite(admin.AdminSite):
    """Custom admin site with improved navigation structure"""
    site_header = _("Quality Tools Administration")
    site_title = _("Quality Tools Admin")
    index_title = _("Dashboard")

    def get_app_list(self, request):
        """
        Override to group apps into categories.
        """
        app_dict = self._build_app_dict(request)
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())
        
        # Admin navigation categories as defined in project guidelines
        categories = {
            'auth': {
                'name': _('Authentication and Authorization'),
                'models': [],
                'icon': 'fa-shield-alt'
            },
            'company': {
                'name': _('Companies'),
                'models': [],
                'icon': 'fa-building'
            },
            'equipment': {
                'name': _('Equipment Management'),
                'models': [],
                'icon': 'fa-tools'
            },
            'quality_docs': {
                'name': _('Management Documentation'),
                'models': [],
                'icon': 'fa-file-alt'
            },
            'personnel': {
                'name': _('Personnel Management'),
                'models': [],
                'icon': 'fa-users'
            },
            'standards': {
                'name': _('Standards'),
                'models': [],
                'icon': 'fa-clipboard-list'
            },
            'accounts': {
                'name': _('User Accounts'),
                'models': [],
                'icon': 'fa-user-cog'
            },
            'other': {
                'name': _('Other Applications'),
                'models': [],
                'icon': 'fa-th'
            },
        }
        
        # Assign models to their categories
        for app in app_list:
            app_name = app['app_label']
            if app_name in categories:
                categories[app_name]['models'].extend(app['models'])
            else:
                categories['other']['models'].extend(app['models'])
        
        # Create the final ordered list
        categorized_list = []
        for key, category in categories.items():
            if category['models']:
                category_dict = {
                    'name': category['name'],
                    'app_label': key,
                    'app_url': f"#app_{key}",
                    'has_module_perms': True,
                    'models': sorted(category['models'], key=lambda x: x['name']),
                    'is_category': True,
                    'icon': category['icon']
                }
                categorized_list.append(category_dict)
        
        return categorized_list

# Create a custom admin site instance to replace the default one
custom_admin_site = CustomAdminSite(name='admin')

# Function to register models in the admin
def register_models_admin(app_models, site=admin.site, **options):
    """Helper function to register multiple models with the same options"""
    for model in app_models:
        site.register(model, **options)
