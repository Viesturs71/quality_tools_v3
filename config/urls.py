"""URL Configuration for the project."""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.i18n import set_language

from apps.users.views import home_view

urlpatterns = [
    # Standard language switcher
    path('i18n/setlang/', set_language, name='set_language'),

    # Rosetta translation tool
    path('rosetta/', include('rosetta.urls')),

    # Django's built-in auth
    path('accounts/', include('django.contrib.auth.urls')),

    # Admin panel
    path('admin/', admin.site.urls),

    # Your apps
    path('users/', include('apps.users.urls', namespace='users')),
    path('documents/', include('apps.documents.urls', namespace='documents_app')),
    path('equipment/', include('apps.equipment.urls', namespace='equipment_app')),
    path('dashboard/', include('apps.dashboard.urls', namespace='dashboard')),
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('personnel/', include('apps.personnel.urls', namespace='personnel')),
    path('standards/', include('apps.standards.urls', namespace='standards')),
    path('debug/', include('apps.debug_tools.urls')),  # Debug tools URLs

    # Home page
    path('', home_view, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG and 'debug_toolbar' in settings.INSTALLED_APPS:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
