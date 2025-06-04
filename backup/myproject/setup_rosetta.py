import os
import subprocess
from pathlib import Path


def main():
    """Configure Rosetta and translations properly"""
    BASE_DIR = Path(__file__).resolve().parent

    # 1. Create locale directory in the correct location
    locale_dir = BASE_DIR / 'locale'
    os.makedirs(locale_dir, exist_ok=True)

    # 2. Create standard language directories
    for lang in ['lv', 'de', 'es']:
        os.makedirs(locale_dir / lang / 'LC_MESSAGES', exist_ok=True)

    # 3. Create translation strings file
    with open(BASE_DIR / "translation_strings.py", 'w', encoding='utf-8') as f:
        f.write('''
from django.utils.translation import gettext_lazy as _

# Common terms for translation
_("Home")
_("Dashboard")
_("Settings")
_("Profile")
_("Login")
_("Logout")
_("Register")
_("Save")
_("Cancel")
_("Delete")
_("Edit")
_("Create")
_("Search")
_("Filter")

# Equipment terms
_("Equipment")
_("Measuring Instrument")
_("Calibration")
_("Verification")
_("Metrological Control")
_("Equipment Registry")
_("Inventory Number")
_("Serial Number")
_("Model")
_("Manufacturer")
_("Purchase Date")

# Document terms
_("Document")
_("Standard")
_("Procedure")
''')

    # 4. Update settings.py to ensure correct locale paths
    settings_path = BASE_DIR / 'myproject' / 'settings.py'
    with open(settings_path, encoding='utf-8') as f:
        settings = f.read()

    if "os.path.join(BASE_DIR, \"myproject\", \"locale\")" in settings:
        settings = settings.replace(
            "os.path.join(BASE_DIR, \"myproject\", \"locale\")",
            "os.path.join(BASE_DIR, \"locale\")"
        )
        with open(settings_path, 'w', encoding='utf-8') as f:
            f.write(settings)

    # 5. Run makemessages for each language with proper encoding
    os.environ['PYTHONIOENCODING'] = 'utf-8'

    for lang in ['lv', 'de', 'es']:
        result = subprocess.run([
            'python', 'manage.py', 'makemessages',
            '-l', lang,
            '--ignore=venv/*',
            '--ignore=env/*',
            '--extension=py,html,txt'
        ], capture_output=True, text=True)

        if result.stderr:
            pass

    # 6. Compile messages
    result = subprocess.run([
        'python', 'manage.py', 'compilemessages'
    ], capture_output=True, text=True)

    if result.stderr:
        pass

    # 7. Clean up
    if os.path.exists(BASE_DIR / "translation_strings.py"):
        os.unlink(BASE_DIR / "translation_strings.py")


if __name__ == "__main__":
    main()
