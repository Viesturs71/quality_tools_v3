import os
import subprocess


def main():
    """Create and initialize translation files in the correct location"""
    # Ensure directory structure exists
    locale_dir = os.path.join('myproject', 'locale')
    os.makedirs(locale_dir, exist_ok=True)

    # Create a dummy file with some translatable content
    with open('dummy_translations.py', 'w', encoding='utf-8') as f:
        f.write('''
# This file exists only to provide strings for translation
from django.utils.translation import gettext_lazy as _

def get_translatable_strings():
    """Returns translatable strings for the translation system"""
    return {
        'general': {
            'equipment': _('Equipment'),
            'documents': _('Documents'),
            'users': _('Users'),
            'settings': _('Settings'),
        },
        'equipment': {
            'add_equipment': _('Add Equipment'),
            'edit_equipment': _('Edit Equipment'),
            'delete_equipment': _('Delete Equipment'),
            'equipment_list': _('Equipment List'),
            'measuring_instrument': _('Measuring Instrument'),
            'calibration': _('Calibration'),
            'verification': _('Verification'),
        },
        'documents': {
            'add_document': _('Add Document'),
            'edit_document': _('Edit Document'),
            'delete_document': _('Delete Document'),
            'document_list': _('Document List'),
            'approve': _('Approve'),
            'reject': _('Reject'),
        },
    }

# Call the function to ensure the strings are recognized
strings = get_translatable_strings()
        ''')

    # Create translation files for each language
    languages = ['lv', 'de', 'es']

    for lang in languages:
        subprocess.run([
            'django-admin', 'makemessages',
            '-l', lang,
            '--extension=py,html,txt',
            '--locale=myproject/locale'
        ], check=True)

    # Compile all messages
    subprocess.run([
        'django-admin', 'compilemessages',
        '--locale=myproject/locale'
    ], check=True)


    # Clean up
    if os.path.exists('dummy_translations.py'):
        os.unlink('dummy_translations.py')

if __name__ == "__main__":
    main()
