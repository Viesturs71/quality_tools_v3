"""URL Configuration for the project."""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language

from apps.users.views import home_view

urlpatterns = [
     # language-switcher for {% url 'set_language' %}
     path('i18n/', include('django.conf.urls.i18n')),
     # register Rosetta under the “rosetta” namespace
     path('rosetta/', include(('rosetta.urls', 'rosetta'), namespace='rosetta')),
     # django’s built-in auth (login/logout/password reset)
     path('accounts/', include('django.contrib.auth.urls')),
     path('set-language/', set_language, name='set_language'),  # Ensure this is included
 ]

urlpatterns += i18n_patterns(
    # Admin panel
    path('admin/', admin.site.urls),

    # Your apps
    path('users/', include('apps.users.urls', namespace='users')),
    path('documents/', include('apps.documents.urls', namespace='documents_app')),
    path('equipment/', include('apps.equipment.urls', namespace='equipment_app')),
    path('dashboard/', include('apps.dashboard.urls', namespace='dashboard')),
    path('accounts/', include('apps.accounts.urls',    namespace='accounts')),
    path('personnel/', include('apps.personnel.urls', namespace='personnel')),
    path('standards/', include('apps.standards.urls', namespace='standards')),

    # Home page (no prefix when default language)
    path('', home_view, name='home'),

    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
