"""
URL configuration for Quality Tools project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    # Non-i18n patterns
    path('i18n/', include('django.conf.urls.i18n')),
]

# Patterns with i18n
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('users/', include('apps.users.urls')),
    path('documents/', include('apps.documents.urls')),
    path('equipment/', include('apps.equipment.urls')),
    path('personnel/', include('apps.personnel.urls')),
    path('company/', include('apps.company.urls')),
    path('standards/', include('apps.standards.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('methods/', include('apps.methods.urls')),
    prefix_default_language=True
)

# Add Rosetta URLs if it's installed
if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        path('rosetta/', include('rosetta.urls')),
    ]

# Serve media and static files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    # Add debug toolbar URLs if it's installed
    try:
        import debug_toolbar
        urlpatterns += [
            path('__debug__/', include(debug_toolbar.urls)),
        ]
    except ImportError:
        pass
