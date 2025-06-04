"""
This script marks the specified migration as applied in the database
without actually running it. This is useful for resolving migration conflicts
when the database already has the changes but the migration history is inconsistent.
"""
import os
import sys

import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.db import connection
from django.db.migrations.recorder import MigrationRecorder


def mark_migration_as_applied(app, migration_name):
    """Mark a migration as applied in the database."""
    recorder = MigrationRecorder(connection)

    # Check if the migration already exists
    if not recorder.migration_qs.filter(app=app, name=migration_name).exists():
        recorder.record_applied(app, migration_name)
    else:
        pass

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(1)

    app_name = sys.argv[1]
    migration_name = sys.argv[2]

    mark_migration_as_applied(app_name, migration_name)
