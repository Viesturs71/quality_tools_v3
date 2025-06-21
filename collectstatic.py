import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

# Create static directories if they don't exist
from django.conf import settings

static_dir = os.path.join(settings.BASE_DIR, 'static')
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

admin_css_dir = os.path.join(static_dir, 'admin', 'css')
if not os.path.exists(admin_css_dir):
    os.makedirs(admin_css_dir)

admin_js_dir = os.path.join(static_dir, 'admin', 'js')
if not os.path.exists(admin_js_dir):
    os.makedirs(admin_js_dir)

print("Created static directories")

# Now run collectstatic
from django.core.management import call_command
call_command('collectstatic', interactive=False)

print("Static files collected successfully")
