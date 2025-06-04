import subprocess


def main():
    """Create migrations for equipment app"""

    # Run makemigrations for equipment app
    result = subprocess.run(
        ['python', 'manage.py', 'makemigrations', 'equipment'],
        capture_output=True,
        text=True,
        check=False
    )

    if result.stderr:
        pass

    # Run migrate to apply migrations
    result = subprocess.run(
        ['python', 'manage.py', 'migrate'],
        capture_output=True,
        text=True,
        check=False
    )

    if result.stderr:
        pass


if __name__ == "__main__":
    main()
