"""
Script to apply migrations with --fake-initial flag for existing tables.
"""
import os
import subprocess

def run_fake_initial_migrations():
    """Apply migrations with --fake-initial flag."""
    print("Running migrations with --fake-initial flag...")
    
    # Run the migrate command with fake-initial flag
    result = subprocess.run(
        ["python", "manage.py", "migrate", "--fake-initial"],
        capture_output=True,
        text=True
    )
    
    # Print output
    print(result.stdout)
    
    if result.returncode != 0:
        print("Error running migrations:")
        print(result.stderr)
        return False
    
    print("Fake-initial migrations completed.")
    return True

if __name__ == "__main__":
    print("This script will apply migrations with --fake-initial flag.")
    print("This is useful when tables already exist in the database.")
    proceed = input("Do you want to proceed? (y/n): ").lower() == 'y'
    
    if proceed:
        run_fake_initial_migrations()
    else:
        print("Operation cancelled.")
