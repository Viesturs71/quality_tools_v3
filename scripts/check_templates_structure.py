#!/usr/bin/env python
"""
Pārbauda veidņu struktūru un includes mapes.
"""

import os
import sys
from pathlib import Path

# Iegūt projekta saknes direktoriju
BASE_DIR = Path(__file__).resolve().parent.parent

def check_template_directories():
    """Pārbauda veidņu direktoriju struktūru."""
    templates_dir = BASE_DIR / 'templates'
    
    print("========== VEIDŅU STRUKTŪRAS PĀRBAUDE ==========")
    
    # Pārbaudīt vai templates mape eksistē
    if not templates_dir.exists():
        print(f"❌ 'templates' mape nav atrasta: {templates_dir}")
        return
    
    print(f"✅ 'templates' mape atrasta: {templates_dir}")
    
    # Saraksts ar meklējamajām veidņu mapēm
    template_dirs = [
        'admin',
        'users',
        'dashboard',
        'equipment',
        'quality_docs',
        'standards',
        'personnel',
        'companies',
    ]
    
    for template_dir in template_dirs:
        dir_path = templates_dir / template_dir
        if not dir_path.exists():
            print(f"❌ 'templates/{template_dir}' mape nav atrasta")
            os.makedirs(dir_path, exist_ok=True)
            print(f"✅ Izveidota 'templates/{template_dir}' mape")
        else:
            print(f"✅ 'templates/{template_dir}' mape atrasta")
        
        # Pārbaudīt vai ir includes mape
        includes_dir = dir_path / 'includes'
        if not includes_dir.exists():
            print(f"❌ 'templates/{template_dir}/includes' mape nav atrasta")
            os.makedirs(includes_dir, exist_ok=True)
            print(f"✅ Izveidota 'templates/{template_dir}/includes' mape")
        else:
            print(f"✅ 'templates/{template_dir}/includes' mape atrasta")
    
    print("\n========== NEPIECIEŠAMO VEIDŅU FAILU PĀRBAUDE ==========")
    
    # Pārbaudīt svarīgākos veidņu failus
    key_templates = {
        'admin/base_admin.html': 'Administratora bāzes veidne',
        'admin/includes/admin_header.html': 'Administratora galvene',
        'admin/includes/admin_navigation.html': 'Administratora navigācija',
        'users/base_user.html': 'Lietotāja bāzes veidne',
        'users/includes/user_header.html': 'Lietotāja galvene',
        'users/includes/user_navigation.html': 'Lietotāja navigācija',
        'dashboard/index.html': 'Kontrolpaneļa sākumlapa',
    }
    
    for template_path, description in key_templates.items():
        file_path = templates_dir / template_path
        if not file_path.exists():
            print(f"❌ '{template_path}' nav atrasts - {description}")
        else:
            print(f"✅ '{template_path}' atrasts - {description}")
    
    print("\n========== INCLUDES FAILU SATURA PĀRBAUDE ==========")
    
    # Pārbaudīt vai ir atbilstošs saturs includes failos
    includes_to_check = [
        ('admin/includes/admin_header.html', '<header'),
        ('admin/includes/admin_navigation.html', '<nav'),
        ('users/includes/user_header.html', '<header'),
        ('users/includes/user_navigation.html', '<nav'),
    ]
    
    for template_path, expected_content in includes_to_check:
        file_path = templates_dir / template_path
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if expected_content in content:
                        print(f"✅ '{template_path}' satur pareizu struktūru")
                    else:
                        print(f"❌ '{template_path}' nesatur pareizu struktūru")
            except Exception as e:
                print(f"❌ Kļūda lasot '{template_path}': {str(e)}")
        else:
            print(f"❌ '{template_path}' nav atrasts vai nav pieejams")

if __name__ == "__main__":
    check_template_directories()
