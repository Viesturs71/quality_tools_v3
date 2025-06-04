# main
import sys

from django.core.management import execute_from_command_line


def main():
    """
    Galvenā ieejas funkcija Django projektam.
    """
    try:
        execute_from_command_line(sys.argv)
    except Exception:
        pass


if __name__ == "__main__":
    main()
