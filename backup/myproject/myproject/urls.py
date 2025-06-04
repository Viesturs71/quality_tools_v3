## 🌐 **`myprojects/urls.py`**
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),  # Add this line to include language change URLs
    path('', include('dashboard.urls')),  # No namespace for the main app
    path('equipment/', include('equipment.urls', namespace='equipment')),

    # Placeholder URLs for other apps (to be implemented)
    # path('documents/', include('documents.urls', namespace='documents')),
    # path('personnel/', include('personnel.urls', namespace='personnel')),
    # path('standards/', include('standards.urls', namespace='standards')),

    # Static pages with generic views
    path('about/', TemplateView.as_view(template_name='pages/about.html'), name='about'),
    path('privacy/', TemplateView.as_view(template_name='pages/privacy.html'), name='privacy'),
    path('terms/', TemplateView.as_view(template_name='pages/terms.html'), name='terms'),
    path('contact/', TemplateView.as_view(template_name='pages/contact.html'), name='contact'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
