import os
import subprocess
from pathlib import Path


def main():
    """Set up translation files correctly"""
    BASE_DIR = Path(__file__).resolve().parent

    # 1. Create proper locale directory structure
    locale_dir = BASE_DIR / "locale"
    os.makedirs(locale_dir, exist_ok=True)

    for lang in ['lv', 'de', 'es']:
        os.makedirs(locale_dir / lang / "LC_MESSAGES", exist_ok=True)

    # 2. Create translation strings file
    with open(BASE_DIR / "translation_strings.py", 'w', encoding='utf-8') as f:
        f.write('''
# This file contains translatable strings
from django.utils.translation import gettext_lazy as _

# Basic UI terms
TERMS = {
    # Common terms
    "home": _("Home"),
    "dashboard": _("Dashboard"),
    "settings": _("Settings"),
    "profile": _("Profile"),
    "logout": _("Logout"),
    "login": _("Login"),
    "register": _("Register"),
    "save": _("Save"),
    "cancel": _("Cancel"),
    "delete": _("Delete"),
    "edit": _("Edit"),
    "create": _("Create"),
    "search": _("Search"),
    "filter": _("Filter"),

    # Equipment terms
    "equipment": _("Equipment"),
    "measuring_instrument": _("Measuring Instrument"),
    "calibration": _("Calibration"),
    "verification": _("Verification"),
    "metrological_control": _("Metrological Control"),
    "equipment_registry": _("Equipment Registry"),
    "inventory_number": _("Inventory Number"),
    "serial_number": _("Serial Number"),
    "model": _("Model"),
    "manufacturer": _("Manufacturer"),
    "purchase_date": _("Purchase Date"),

    # Document terms
    "document": _("Document"),
    "standard": _("Standard"),
    "procedure": _("Procedure"),
}
''')

    # 3. Run makemessages (avoid circular imports during this process)
    for lang in ['lv', 'de', 'es']:
        subprocess.run([
            'python', 'manage.py', 'makemessages',
            '-l', lang,
            '--ignore=venv/*',
            '--ignore=env/*',
            '--extension=py,html,txt'
        ], check=True)

    # 4. Compile messages
    subprocess.run(['python', 'manage.py', 'compilemessages'], check=True)


    # Clean up
    os.remove(BASE_DIR / "translation_strings.py")

if __name__ == "__main__":
    main()
