#!/usr/bin/env python3
import subprocess
import sys
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def run_html_validity():
    print("\n" + "="*10 + " HTML5 VALIDATION " + "="*10)
    # Ensure Java is available
    if not shutil.which("java"):
        print("✘ java not found. Please install a JRE (e.g. Temurin) and add it to PATH.")
        return False
    # Ensure html5validator CLI is available
    if not shutil.which("html5validator"):
        print("✘ html5validator CLI not found. Run:\n    pip install html5validator")
        return False

    cmd = ["html5validator", "--root", "templates", "--format", "text"]
    result = subprocess.run(cmd, capture_output=True, text=True, shell=(sys.platform=="win32"))
    if result.returncode == 0:
        print("✔ HTML5 validation passed")
        return True
    else:
        print("✘ HTML5 validation failed:\n")
        print(result.stdout or result.stderr)
        return False

def run_html_lint():
    print("\n" + "="*10 + " HTML LINTING " + "="*10)
    if not shutil.which("npx"):
        print("✘ npx not found. Please `npm install --save-dev htmlhint`")
        return False

    cmd = ["npx", "htmlhint", "templates/**/*.html"]
    result = subprocess.run(cmd, capture_output=True, text=True, shell=(sys.platform=="win32"))
    if result.returncode == 0:
        print("✔ HTMLHint passed")
        return True
    print("✘ HTMLHint found issues:\n", result.stdout or result.stderr)
    return False

def run_accessibility():
    print("\n" + "="*10 + " ACCESSIBILITY (Pa11y) " + "="*10)
    if not shutil.which("npx"):
        print("✘ npx not found. Please `npm install --save-dev pa11y`")
        return False

    cmd = ["npx", "pa11y", "http://localhost:8000/admin/"]
    result = subprocess.run(cmd, capture_output=True, text=True, shell=(sys.platform=="win32"))
    if result.returncode == 0:
        print("✔ Pa11y accessibility checks passed")
        return True
    print("✘ Pa11y found accessibility issues:\n", result.stdout or result.stderr)
    return False

def run_ui_tests():
    print("\n" + "="*10 + " SELENIUM UI TESTS " + "="*10)
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

    def check(cond, msg):
        nonlocal failures
        if cond:
            print("✔", msg)
        else:
            print("✘", msg)
            failures += 1

    # 1) Index redirects to login
    driver.get("http://localhost:8000/admin/")
    check("/admin/login/" in driver.current_url, "Admin index redirects to login")

    # 2) Custom site title in <title>
    for path in ["/admin/", "/admin/login/"]:
        driver.get(f"http://localhost:8000{path}")
        check("Management System Tools Admin" in driver.title,
              f"Site title at {path!r}: {driver.title!r}")

    # 3) Branding H1 on login
    driver.get("http://localhost:8000/admin/login/")
    h1s = [h.text for h in driver.find_elements("tag name", "h1")]
    check("Log in" in h1s,  # Updated expected text
          f"Branding H1 on login (found {h1s})")

    driver.quit()
    return failures == 0

def main():
    overall = True
    overall &= run_html_validity()
    overall &= run_html_lint()
    overall &= run_accessibility()
    overall &= run_ui_tests()

    print("\n" + "="*5 + " SUMMARY " + "="*5)
    if overall:
        print("🎉 All checks passed!")
        sys.exit(0)
    else:
        print("❗ Some checks failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
