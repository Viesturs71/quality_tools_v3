#!/usr/bin/env python3
import subprocess
import sys
import shutil
from html5validator import validate
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def run_html_validity():
    print("\n" + "="*10 + " HTML5 VALIDATION " + "="*10)
    try:
        # will raise AssertionError if any file is invalid
        validate(root='templates', format='text')
        print("✔ HTML5 validation passed")
    except AssertionError as e:
        print("✘ HTML5 validation failed:")
        print(e)
        return False
    return True

def run_html_lint():
    print("\n" + "="*10 + " HTML LINTING " + "="*10)
    if not shutil.which("npx"):
        print("✘ npx not found. Please `npm install htmlhint --save-dev`")
        return False
    cmd = ["npx", "htmlhint", "templates/**/*.html"]
    result = subprocess.run(cmd, capture_output=True, text=True, shell=(sys.platform=="win32"))
    if result.returncode == 0:
        print("✔ HTMLHint passed")
        return True
    else:
        print("✘ HTMLHint found issues:")
        print(result.stdout or result.stderr)
        return False

def run_accessibility():
    print("\n" + "="*10 + " ACCESSIBILITY (Pa11y) " + "="*10)
    if not shutil.which("npx"):
        print("✘ npx not found. Please `npm install pa11y --save-dev`")
        return False
    # make sure your Django dev server is running at localhost:8000
    cmd = ["npx", "pa11y", "http://localhost:8000/admin/"]
    result = subprocess.run(cmd, capture_output=True, text=True, shell=(sys.platform=="win32"))
    if result.returncode == 0:
        print("✔ Pa11y accessibility checks passed")
        return True
    else:
        print("✘ Pa11y found accessibility issues:")
        print(result.stdout or result.stderr)
        return False

def run_ui_tests():
    print("\n" + "="*10 + " SELENIUM UI TESTS " + "="*10)
    # headless Chrome
    opts = webdriver.ChromeOptions()
    opts.add_argument("--headless")
    try:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=opts
        )
    except Exception as e:
        print("✘ Failed to start Chrome WebDriver:", e)
        return False

    driver.implicitly_wait(5)
    failures = 0

    def assert_(cond, msg):
        nonlocal failures
        if cond:
            print("✔", msg)
        else:
            print("✘", msg)
            failures += 1

    # Test 1: redirect from /admin/ to /admin/login/
    driver.get("http://localhost:8000/admin/")
    assert_( "/admin/login/" in driver.current_url,
             "Admin index redirects to login" )

    # Test 2: page title contains custom site_title
    for path in ["/admin/", "/admin/login/"]:
        driver.get(f"http://localhost:8000{path}")
        title = driver.title
        assert_( "Management System Tools Admin" in title,
                  f"Site title on {path}: '{title}'" )

    # Test 3: login page shows branding <h1>
    driver.get("http://localhost:8000/admin/login/")
    h1s = [h.text for h in driver.find_elements("tag name", "h1")]
    assert_( "Management System Tools" in h1s,
             f"Branding H1 on login page: found {h1s}" )

    driver.quit()
    return failures == 0

def main():
    overall = True

    # 1) HTML validity
    if not run_html_validity():
        overall = False

    # 2) HTML lint
    if not run_html_lint():
        overall = False

    # 3) Accessibility
    if not run_accessibility():
        overall = False

    # 4) UI tests
    if not run_ui_tests():
        overall = False

    print("\n" + "="*5 + " SUMMARY " + "="*5)
    if overall:
        print("🎉 All checks passed!")
        sys.exit(0)
    else:
        print("❗ Some checks failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
