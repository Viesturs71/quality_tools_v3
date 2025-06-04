#!/usr/bin/env python
"""
Pārbauda, vai veidņu struktūra atbilst projekta prasībām.
Visām veidnēm jāatrodas templates/[app_name]/ mapē.
"""

import os
import sys
from pathlib import Path

# Iegūt projekta saknes direktoriju
BASE_DIR = Path(__file__).resolve().parent.parent

def check_templates_structure():
    """Pārbauda veidņu struktūru un izdrukā rezultātus."""
    templates_dir = BASE_DIR / 'templates'
    
    if not templates_dir.exists():
        print(f"❌ 'templates' mape nav atrasta: {templates_dir}")
        return False
    
    print("✅ 'templates' mape atrasta")
    
    # Iegūt visas Django aplikācijas (mapes ar models.py failu)
    apps = []
    for item in BASE_DIR.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            models_file = item / 'models.py'
            models_dir = item / 'models'
            if models_file.exists() or models_dir.exists():
                apps.append(item.name)
    
    # Pārbaudīt, vai katrai aplikācijai ir atbilstoša templates/[app_name] mape
    all_valid = True
    for app in apps:
        app_templates_dir = templates_dir / app
        if app_templates_dir.exists():
            print(f"✅ 'templates/{app}' mape atrasta")
            
            # Pārbaudīt, vai ir vismaz viena veidne
            templates_count = sum(1 for _ in app_templates_dir.glob('**/*.html'))
            if templates_count > 0:
                print(f"  ✅ Atrasti {templates_count} veidņu faili")
            else:
                print(f"  ❌ Nav atrasti veidņu faili")
                all_valid = False
        else:
            print(f"❌ 'templates/{app}' mape nav atrasta")
            all_valid = False
    
    # Pārbaudīt, vai nav veidņu mapē mapes, kas neattiecas uz aplikācijām
    for item in templates_dir.iterdir():
        if item.is_dir() and item.name not in apps and item.name != 'admin':
            print(f"⚠️ Aizdomīga mape 'templates/{item.name}' - neattiecas uz esošām aplikācijām")
    
    return all_valid

if __name__ == "__main__":
    print("\n========== PĀRBAUDE: VEIDŅU STRUKTŪRA ==========")
    success = check_templates_structure()
    print("\n========== REZULTĀTS ==========")
    if success:
        print("✅ Veidņu struktūra atbilst prasībām")
        sys.exit(0)
    else:
        print("❌ Veidņu struktūra NEATBILST prasībām")
        sys.exit(1)
