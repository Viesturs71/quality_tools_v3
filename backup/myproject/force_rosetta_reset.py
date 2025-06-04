import os
import subprocess
from pathlib import Path

import django
from django.conf import settings

# Initialize Django to access settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

def main():
    """Force Rosetta to refresh by recreating all translation files"""
    BASE_DIR = Path(__file__).resolve().parent

    # 1. Get locale paths from settings
    locale_paths = getattr(settings, "LOCALE_PATHS", [])
    if not locale_paths:
        locale_paths = [os.path.join(BASE_DIR, "locale")]


    # 2. Create minimal translation strings
    with open(BASE_DIR / "force_translations.py", "w", encoding="utf-8") as f:
        f.write('from django.utils.translation import gettext_lazy as _\n')
        f.write('_("Hello")\n')
        f.write('_("World")\n')
        f.write('_("Rosetta")\n')
        f.write('_("Translation")\n')

    # 3. Generate translations
    os.environ["PYTHONIOENCODING"] = "utf-8"

    for lang in ["lv", "de", "es"]:
        cmd = [
            "python", "manage.py", "makemessages",
            "-l", lang,
            "--ignore=venv/*",
            "--extension=py,html,txt",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.stderr:
            pass

    # 4. Compile messages
    subprocess.run(["python", "manage.py", "compilemessages"])

    # 5. Clean up
    if os.path.exists(BASE_DIR / "force_translations.py"):
        os.unlink(BASE_DIR / "force_translations.py")


if __name__ == "__main__":
    main()
