from django.shortcuts import render
from django.urls import get_resolver
from django.conf import settings
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _


def debug_urls(request):
    """View to display all available URL names in the project."""
    resolver = get_resolver()
    url_patterns = resolver.url_patterns
    
    url_names = []
    def extract_url_names(patterns):
        for pattern in patterns:
            if hasattr(pattern, 'name') and pattern.name:
                url_names.append(pattern.name)
            if hasattr(pattern, 'url_patterns'):
                extract_url_names(pattern.url_patterns)
    
    extract_url_names(url_patterns)
    url_names.sort()
    
    return render(request, 'debug/urls.html', {'url_names': url_names})


def debug_template_dirs(request):
    """
    Debug view to check template directories configuration.
    Shows template directories, static files directories, and checks admin template existence.
    """
    template_dirs = settings.TEMPLATES[0]['DIRS']
    staticfiles_dirs = settings.STATICFILES_DIRS
    
    response = f"""
    <h1>Debug Template Configuration</h1>
    <h2>Template Directories:</h2>
    <ul>
        {''.join(f'<li>{dir}</li>' for dir in template_dirs)}
    </ul>
    
    <h2>Static Files Directories:</h2>
    <ul>
        {''.join(f'<li>{dir}</li>' for dir in staticfiles_dirs)}
    </ul>
    
    <h2>Admin Templates:</h2>
    <p>Path to admin base_site.html should be: {settings.BASE_DIR / 'templates' / 'admin' / 'base_site.html'}</p>
    <p>File exists: {(settings.BASE_DIR / 'templates' / 'admin' / 'base_site.html').exists()}</p>
    """
    
    return HttpResponse(response)


def debug_settings(request):
    """
    Debug view to display important Django settings.
    This is useful for verifying configuration across environments.
    """
    # Only show non-sensitive settings
    safe_settings = {
        'DEBUG': settings.DEBUG,
        'ALLOWED_HOSTS': settings.ALLOWED_HOSTS,
        'INSTALLED_APPS': settings.INSTALLED_APPS,
        'MIDDLEWARE': settings.MIDDLEWARE,
        'DATABASES': {'default': {'ENGINE': settings.DATABASES['default']['ENGINE']}},
        'LANGUAGE_CODE': settings.LANGUAGE_CODE,
        'TIME_ZONE': settings.TIME_ZONE,
        'USE_I18N': settings.USE_I18N,
        'USE_TZ': settings.USE_TZ,
        'STATIC_URL': settings.STATIC_URL,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    
    response = """
    <h1>Debug Django Settings</h1>
    <style>
        .key { font-weight: bold; color: #336699; }
        .value { margin-left: 20px; }
        .setting { margin-bottom: 10px; }
    </style>
    """
    
    for key, value in safe_settings.items():
        response += f'<div class="setting"><span class="key">{key}:</span> <div class="value"><pre>{value}</pre></div></div>'
    
    return HttpResponse(response)