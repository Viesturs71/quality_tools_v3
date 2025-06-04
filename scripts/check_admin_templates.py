#!/usr/bin/env python
"""
Pārbauda admin veidņu struktūru un integritāti.
"""

import os
import sys
from pathlib import Path

# Iegūt projekta saknes direktoriju
BASE_DIR = Path(__file__).resolve().parent.parent

def check_admin_templates():
    """Pārbauda admin veidņu struktūru un izdrukā rezultātus."""
    templates_dir = BASE_DIR / 'templates'
    admin_templates_dir = templates_dir / 'admin'
    
    print("========== ADMIN VEIDŅU PĀRBAUDE ==========")
    
    # Pārbaudīt vai templates mape eksistē
    if not templates_dir.exists():
        print(f"❌ 'templates' mape nav atrasta: {templates_dir}")
        os.makedirs(templates_dir, exist_ok=True)
        print(f"✅ Izveidota 'templates' mape: {templates_dir}")
    else:
        print(f"✅ 'templates' mape atrasta: {templates_dir}")
    
    # Pārbaudīt vai admin mape eksistē
    if not admin_templates_dir.exists():
        print(f"❌ 'templates/admin' mape nav atrasta: {admin_templates_dir}")
        os.makedirs(admin_templates_dir, exist_ok=True)
        print(f"✅ Izveidota 'templates/admin' mape: {admin_templates_dir}")
    else:
        print(f"✅ 'templates/admin' mape atrasta: {admin_templates_dir}")
    
    # Pārbaudīt admin veidņu struktūru
    admin_templates = list(admin_templates_dir.glob('*.html'))
    if not admin_templates:
        print("❌ 'templates/admin' mapē nav atrasta neviena .html veidne")
    else:
        print(f"✅ Atrastas {len(admin_templates)} admin veidnes:")
        for template in admin_templates:
            print(f"   - {template.name}")
    
    # Pārbaudīt base_admin.html
    base_admin_path = admin_templates_dir / 'base_admin.html'
    if not base_admin_path.exists():
        print("❌ 'base_admin.html' veidne nav atrasta")
    else:
        print("✅ 'base_admin.html' veidne atrasta")
        
        # Pārbaudīt DOCTYPE deklarāciju
        with open(base_admin_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if '<!DOCTYPE html>' in content:
                print("✅ 'base_admin.html' satur DOCTYPE deklarāciju")
            else:
                print("❌ 'base_admin.html' nesatur DOCTYPE deklarāciju")
            
            # Pārbaudīt header daļu
            if '<header' in content:
                print("✅ 'base_admin.html' satur header daļu")
            else:
                print("❌ 'base_admin.html' nesatur header daļu")
            
            # Pārbaudīt includes
            includes = []
            for line in content.split('\n'):
                if '{% include' in line:
                    include_path = line.split('{% include')[1].split('%}')[0].strip().strip('"\'')
                    includes.append(include_path)
            
            if includes:
                print(f"✅ Atrasti {len(includes)} includes:")
                for include in includes:
                    include_path = templates_dir / include.lstrip('/')
                    if include_path.exists():
                        print(f"   ✅ {include} - atrasts")
                    else:
                        print(f"   ❌ {include} - nav atrasts")
            else:
                print("❌ Nav atrasts neviens include")
    
    print("\n========== REZULTĀTS ==========")
    if admin_templates_dir.exists() and list(admin_templates_dir.glob('*.html')):
        print("✅ Admin veidnes ir pieejamas")
    else:
        print("❌ Admin veidnes NAV pieejamas vai ir nepilnīgas")

if __name__ == "__main__":
    check_admin_templates()
