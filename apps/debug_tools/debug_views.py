from django.conf import settings
from django.http import HttpResponse

def debug_template_dirs(request):
    """Debug view to check template directories configuration."""
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
