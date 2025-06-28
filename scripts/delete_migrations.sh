#!/bin/bash
# Delete all migrations from the project

# Check if --backup flag is present
if [[ "$*" == *"--backup"* ]]; then
    BACKUP_FLAG="--backup"
else
    BACKUP_FLAG=""
fi

# Check if --dry-run flag is present
if [[ "$*" == *"--dry-run"* ]]; then
    DRY_RUN_FLAG="--dry-run"
else
    DRY_RUN_FLAG=""
fi

# Check if a specific app was specified
SPECIFIC_APP=""
for arg in "$@"; do
    if [[ $arg != --* ]]; then
        SPECIFIC_APP="--specific-app=$arg"
        break
    fi
done

# Run the management command
echo "Running: python manage.py delete_migrations $BACKUP_FLAG $DRY_RUN_FLAG $SPECIFIC_APP"
python manage.py delete_migrations $BACKUP_FLAG $DRY_RUN_FLAG $SPECIFIC_APP

# If not a dry run, remind to make new migrations
if [[ "$*" != *"--dry-run"* ]]; then
    echo -e "\nNext steps:"
    echo "1. Run 'python manage.py makemigrations' to create new initial migrations"
    echo "2. Run 'python manage.py migrate --fake-initial' to mark migrations as applied without running them"
    echo "   (or delete your database and run 'python manage.py migrate' for a fresh start)"
fi
