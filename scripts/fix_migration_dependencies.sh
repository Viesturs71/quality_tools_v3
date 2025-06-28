#!/bin/bash
# Script to fix migration dependencies and apply migrations in the correct order

# First, show current migration status
echo "Current migration status:"
python manage.py showmigrations

# Run the fix_migrations management command
echo -e "\nFixing migrations..."
python manage.py fix_migrations

# Final check
echo -e "\nFinal migration status:"
python manage.py showmigrations

echo -e "\nIf you still see pending migrations, try running:"
echo "python manage.py migrate"
