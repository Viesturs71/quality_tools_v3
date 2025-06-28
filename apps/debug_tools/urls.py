from django.urls import path
from . import views
from . import language_views

app_name = 'debug_tools'

urlpatterns = [
    # URL pattern debugging
    path('urls/', views.debug_urls, name='debug_urls'),
    
    # Template directory debugging
    path('templates/', views.debug_template_dirs, name='debug_templates'),
    
    # Settings debugging
    path('settings/', views.debug_settings, name='debug_settings'),
    
    # Language switching with confirmation page
    path('set-language/', language_views.custom_set_language, name='set_language'),
]