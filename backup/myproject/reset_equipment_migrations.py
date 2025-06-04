"""
This script helps reset the migration state for the equipment app.
It creates a fresh migration based on the current model state.
"""
import subprocess


def reset_migrations():

    # Ask for confirmation
    confirm = input("This will create a fresh migration based on current models. Continue? (y/n): ")
    if confirm.lower() != 'y':
        return

    # Generate a new migration
    subprocess.run(["python", "manage.py", "makemigrations", "equipment", "--name", "reset_model_state"])



if __name__ == "__main__":
    reset_migrations()
