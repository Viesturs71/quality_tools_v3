"""
Code quality checking script for the Quality Tools project.
Runs linting, security checks, and formatting validation.
"""
import subprocess
import sys
from pathlib import Path


def run_command(command, description):
    """Run a shell command and return success status."""

    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            pass
        return True
    except subprocess.CalledProcessError as e:
        if e.stdout:
            pass
        if e.stderr:
            pass
        return False

def main():
    """Run all code quality checks."""

    # Change to project directory
    Path(__file__).parent.parent

    checks = [
        ("ruff check .", "Running Ruff linter"),
        ("ruff format --check .", "Checking code formatting with Ruff"),
        ("black --check --diff .", "Checking code formatting with Black"),
        ("isort --check-only --diff .", "Checking import sorting with isort"),
        ("pylint --load-plugins=pylint_django --django-settings-module=myproject.settings *.py **/*.py", "Running Pylint analysis"),
        ("bandit -r . -x tests,migrations", "Running Bandit security analysis"),
        ("python manage.py check", "Running Django system checks"),
        ("python manage.py check --deploy", "Running Django deployment checks"),
    ]

    passed = 0
    total = len(checks)

    for command, description in checks:
        if run_command(command, description):
            passed += 1


    if passed == total:
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main())
