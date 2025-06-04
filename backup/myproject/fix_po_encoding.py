import codecs
import os
import re


def fix_po_file(filepath):
    """Fix encoding issues in PO files"""

    # Read the file content
    try:
        with codecs.open(filepath, 'r', encoding='utf-8', errors='replace') as file:
            content = file.read()
    except Exception:
        return

    # Ensure correct Content-Type header
    content = re.sub(
        r'Content-Type: text/plain; charset=.*\\n',
        'Content-Type: text/plain; charset=UTF-8\\n',
        content
    )

    # Write the corrected content back
    try:
        with codecs.open(filepath, 'w', encoding='utf-8') as file:
            file.write(content)
    except Exception:
        pass

def main():
    """Process all PO files in the project."""
    locale_dir = os.path.join(os.getcwd(), 'locale')

    for root, _dirs, files in os.walk(locale_dir):
        for file in files:
            if file.endswith('.po'):
                fix_po_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
