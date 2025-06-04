"""
Code auto-fix script for the Quality Tools project.
Automatically fixes formatting and simple linting issues.
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
    """Run all code auto-fix commands."""

    # Change to project directory
    Path(__file__).parent.parent

    fixes = [
        ("isort .", "Sorting imports with isort"),
        ("black .", "Formatting code with Black"),
        ("ruff check --fix .", "Auto-fixing linting issues with Ruff"),
        ("ruff format .", "Formatting code with Ruff"),
    ]

    fixed = 0
    total = len(fixes)

    for command, description in fixes:
        if run_command(command, description):
            fixed += 1


    if fixed == total:
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main())
