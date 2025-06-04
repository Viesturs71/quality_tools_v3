"""
This script helps fix migration conflicts by marking conflicting migrations as applied
without actually running their SQL commands.
"""
import os

import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.db import connection
from django.db.migrations.recorder import MigrationRecorder


def mark_migration_as_applied(app, migration_name):
    """Mark a migration as applied in the migration history without running it."""
    recorder = MigrationRecorder(connection)
    # Check if the migration already exists
    if not recorder.migration_qs.filter(app=app, name=migration_name).exists():
        recorder.record_applied(app, migration_name)
    else:
        pass

if __name__ == "__main__":
    # Mark these migrations as applied
    mark_migration_as_applied('equipment', 'add_department_model')
    mark_migration_as_applied('equipment', '0001_initial_department')
    mark_migration_as_applied('equipment', '0002_equipment_department_relationship')
    mark_migration_as_applied('equipment', '0002_fix_migrations')

    # Apply the merge migration
    mark_migration_as_applied('equipment', '0003_merge_migrations')

