#!/usr/bin/env python3
import subprocess
import sys
import shutil
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Prepare timestamped report directory
timestamp = datetime.now().strftime('%d%m%y_%H%M')
report_dir = f"tests{timestamp}"
os.makedirs(report_dir, exist_ok=True)
log_path = os.path.join(report_dir, 'report.txt')

# Utility to log to console and file
def log(message='', end='\n'):
    print(message, end=end)
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(message + end)

# -------------------------
# Project Structure Tests
# -------------------------
def run_structure_tests():
    log('\n' + '='*10 + ' PROJECT STRUCTURE TESTS ' + '='*10)
    project_root = os.getcwd()
    entries = os.listdir(project_root)
    apps = [d for d in entries if os.path.isdir(d) and os.path.exists(os.path.join(d, 'apps.py'))]
    failures = 0
    def check(cond, msg):
        nonlocal failures
        if cond:
            log(f"✔ {msg}")
        else:
            log(f"✘ {msg}")
            failures += 1
    if not apps:
        log("✘ No Django apps detected.")
        failures += 1
    for app in apps:
        models_dir = os.path.join(project_root, app, 'models')
        check(os.path.isdir(models_dir), f"'{app}/models' directory exists")
        init_file = os.path.join(models_dir, '__init__.py')
        check(os.path.isfile(init_file), f"'{app}/models/__init__.py' exists")
    templates_root = os.path.join(project_root, 'templates')
    check(os.path.isdir(templates_root), "'templates/' directory exists")
    if os.path.isdir(templates_root):
        for app in apps:
            templ_dir = os.path.join(templates_root, app)
            check(os.path.isdir(templ_dir), f"'templates/{app}' directory exists")
    return failures == 0

# -------------------------
# HTML5 Validation
# -------------------------
def run_html_validity():
    log('\n' + '='*10 + ' HTML5 VALIDATION ' + '='*10)
    if not shutil.which('java'):
        log('✘ java not found. Please install JRE and add to PATH.')
        return False
    if not shutil.which('html5validator'):
        log('✘ html5validator CLI not found. pip install html5validator')
        return False
    cmd = ['html5validator', '--root', 'templates', '--format', 'text']
    result = subprocess.run(cmd, capture_output=True, text=True, shell=(sys.platform=='win32'))
    if result.returncode == 0:
        log('✔ HTML5 validation passed')
        return True
    log('✘ HTML5 validation failed:')
    log(result.stdout or result.stderr)
    return False

# -------------------------
# HTML Linting
# -------------------------
def run_html_lint():
    log('\n' + '='*10 + ' HTML LINTING ' + '='*10)
    if not shutil.which('npx'):
        log('✘ npx not found. npm install --save-dev htmlhint')
        return False
    cmd = ['npx', 'htmlhint', 'templates/**/*.html']
    result = subprocess.run(cmd, capture_output=True, text=True, shell=(sys.platform=='win32'))
    if result.returncode == 0:
        log('✔ HTMLHint passed')
        return True
    log('✘ HTMLHint issues:')
    log(result.stdout or result.stderr)
    return False

# -------------------------
# Accessibility Checks
# -------------------------
def run_accessibility():
    log('\n' + '='*10 + ' ACCESSIBILITY (Pa11y) ' + '='*10)
    if not shutil.which('npx'):
        log('✘ npx not found. npm install --save-dev pa11y')
        return False
    cmd = ['npx', 'pa11y', 'http://localhost:8000/admin/']
    result = subprocess.run(cmd, capture_output=True, text=True, shell=(sys.platform=='win32'))
    if result.returncode == 0:
        log('✔ Pa11y checks passed')
        return True
    log('✘ Pa11y issues:')
    log(result.stdout or result.stderr)
    return False

# -------------------------
# Selenium UI Tests
# -------------------------
def run_ui_tests():
    log('\n' + '='*10 + ' SELENIUM UI TESTS ' + '='*10)
    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless')
    try:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=opts
        )
    except Exception as e:
        log(f'✘ Chrome WebDriver error: {e}')
        return False
    driver.implicitly_wait(5)
    failures = 0
    def check(cond, msg):
        nonlocal failures
        if cond:
            log(f"✔ {msg}")
        else:
            log(f"✘ {msg}")
            failures += 1
    driver.get('http://localhost:8000/admin/')
    check('/admin/login/' in driver.current_url, 'Admin index redirects')
    for path in ['/admin/', '/admin/login/']:
        driver.get(f'http://localhost:8000{path}')
        check('Management System Tools Admin' in driver.title,
              f"Title at {path}: '{driver.title}'")
    driver.get('http://localhost:8000/admin/login/')
    h1s = [h.text for h in driver.find_elements('tag name', 'h1')]
    check('Management System Tools' in h1s, f"Branding H1: {h1s}")
    driver.quit()
    return failures == 0

# -------------------------
# Main
# -------------------------
def main():
    overall = True
    overall &= run_structure_tests()
    overall &= run_html_validity()
    overall &= run_html_lint()
    overall &= run_accessibility()
    overall &= run_ui_tests()
    log('\n' + '='*5 + ' SUMMARY ' + '='*5)
    if overall:
        log('🎉 All checks passed!')
        sys.exit(0)
    else:
        log('❗ Some checks failed.')
        sys.exit(1)

if __name__ == '__main__':
    main()
