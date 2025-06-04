#!/usr/bin/env python
"""
Validē admin veidņu struktūru un HTML atbilstību.
"""

import os
import sys
import re
from pathlib import Path
import html5lib
from html5lib import HTMLParser

# Iegūt projekta saknes direktoriju
BASE_DIR = Path(__file__).resolve().parent.parent

def validate_html(file_path):
    """Pārbauda, vai HTML fails atbilst HTML5 standartam."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        parser = HTMLParser(strict=True)
        parser.parse(content)
        return True, "HTML is valid"
    except Exception as e:
        return False, str(e)

def check_file_exists(file_path):
    """Pārbauda, vai fails eksistē."""
    return file_path.exists()

def validate_admin_templates():
    """Validē admin veidnes un to struktūru."""
    templates_dir = BASE_DIR / 'templates'
    admin_templates_dir = templates_dir / 'admin'
    
    print("========== ADMIN VEIDŅU VALIDĀCIJA ==========")
    
    # Saraksts ar obligātajiem failiem
    required_files = [
        admin_templates_dir / 'base_admin.html',
        admin_templates_dir / 'includes' / 'admin_navigation.html',
        admin_templates_dir / 'includes' / 'admin_header.html',
    ]
    
    # Pārbaudīt, vai visi nepieciešamie faili eksistē
    missing_files = []
    for file_path in required_files:
        if not check_file_exists(file_path):
            missing_files.append(file_path)
            print(f"❌ Trūkst: {file_path.relative_to(BASE_DIR)}")
        else:
            print(f"✅ Atrasts: {file_path.relative_to(BASE_DIR)}")
    
    if missing_files:
        print(f"\n⚠️ Trūkst {len(missing_files)} nepieciešamie faili")
    else:
        print("\n✅ Visi nepieciešamie faili ir atrasti")
    
    # Validēt HTML failus
    print("\n========== HTML5 VALIDĀCIJA ==========")
    for file_path in required_files:
        if file_path.exists():
            valid, message = validate_html(file_path)
            if valid:
                print(f"✅ {file_path.relative_to(BASE_DIR)}: HTML5 valids")
            else:
                print(f"❌ {file_path.relative_to(BASE_DIR)}: HTML5 kļūda")
                print(f"   {message}")
    
    # Pārbaudīt DOCTYPE deklarāciju
    print("\n========== DOCTYPE PĀRBAUDE ==========")
    for file_path in required_files:
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if '<!DOCTYPE html>' in content:
                    print(f"✅ {file_path.relative_to(BASE_DIR)}: Satur DOCTYPE deklarāciju")
                else:
                    print(f"❌ {file_path.relative_to(BASE_DIR)}: Nesatur DOCTYPE deklarāciju")
    
    # Pārbaudīt header elementu
    print("\n========== HEADER PĀRBAUDE ==========")
    base_admin_path = admin_templates_dir / 'base_admin.html'
    if base_admin_path.exists():
        with open(base_admin_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if re.search(r'<header[^>]*>', content):
                print(f"✅ base_admin.html: Satur header elementu")
            else:
                print(f"❌ base_admin.html: Nesatur header elementu")

if __name__ == "__main__":
    validate_admin_templates()
