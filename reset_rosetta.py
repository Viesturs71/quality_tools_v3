import os
import subprocess
from pathlib import Path


def main():
    """Reset and properly initialize Rosetta translations"""
    BASE_DIR = Path(__file__).resolve().parent
    LOCALE_DIR = BASE_DIR / "locale"

    # Step 1: Ensure the locale directory exists with correct structure
    os.makedirs(LOCALE_DIR, exist_ok=True)

    # Step 2: Create language directories
    for lang in ['lv', 'de', 'es']:
        os.makedirs(LOCALE_DIR / lang / "LC_MESSAGES", exist_ok=True)

    # Step 3: Create a file with translatable strings
    with open(BASE_DIR / "translation_strings.py", 'w', encoding='utf-8') as f:
        f.write('''
from django.utils.translation import gettext_lazy as _

# Common UI terms
_("Home")
_("Dashboard")
_("Settings")
_("Profile")
_("Logout")
_("Login")
_("Register")
_("Save")
_("Cancel")
_("Delete")
_("Edit")
_("Create")
_("Search")
_("Filter")

# Equipment related terms
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

# Document related terms
_("Document")
_("Standard")
_("Procedure")
''')

    # Step 4: Clear any existing PO/MO files that might be corrupted
    for pattern in ["*.pot", "*.mo", "*.po~"]:
        for file in LOCALE_DIR.glob(f"**/{pattern}"):
            os.unlink(file)

    # Step 5: Generate fresh translation files with explicit UTF-8 encoding
    os.environ['PYTHONIOENCODING'] = 'utf-8'

    for lang in ['lv', 'de', 'es']:
        subprocess.run([
            'python', 'manage.py', 'makemessages',
            '-l', lang,
            '--ignore=venv/*',
            '--extension=py,html,txt',
        ], check=True)

    # Step 6: Compile messages
    subprocess.run([
        'python', 'manage.py', 'compilemessages'
    ], check=True)

    # Step 7: Clean up
    if os.path.exists(BASE_DIR / "translation_strings.py"):
        os.unlink(BASE_DIR / "translation_strings.py")


if __name__ == "__main__":
    main()
