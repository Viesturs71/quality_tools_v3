## 🌐 **`myprojects/urls.py`**
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView, RedirectView
from myproject.admin import custom_admin_site
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),  # ← klasiskā admin lapa
    path('manage/', custom_admin_site.urls, name='custom_admin'),  # ✅ JAUNA LAPA ar vārdtelpu

    # pārējās lietotnes
    path('accounts/', include('django.contrib.auth.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('', RedirectView.as_view(url='/dashboard/', permanent=False), name='home'),
    
    path('equipment/', include('equipment.urls', namespace='equipment')),
    path('documents/', include('quality_docs.urls', namespace='quality_docs')),
    path('personnel/', include('personnel.urls', namespace='personnel')),
    path('company/', include('company.urls', namespace='company')),
    path('standards/', include('standards.urls', namespace='standards')),
    
    path('i18n/', include('django.conf.urls.i18n')),
    path('rosetta/', include('rosetta.urls')),
    
    path('about/', TemplateView.as_view(template_name='pages/about.html'), name='about'),
    path('privacy/', TemplateView.as_view(template_name='pages/privacy.html'), name='privacy'),
    path('terms/', TemplateView.as_view(template_name='pages/terms.html'), name='terms'),
    path('contact/', TemplateView.as_view(template_name='pages/contact.html'), name='contact'),
]


# Add these URL patterns in debug mode only
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom error handlers
handler404 = 'myproject.views.handler404'
handler500 = 'myproject.views.handler500'
