#!/bin/bash
# Script to fix migration issues with circular dependencies

# Show current migration status
echo "Current migration status:"
python manage.py showmigrations

# Fix migration history first
echo -e "\nFixing migration history..."
python manage.py fix_migration_history

# Apply migrations in correct order
echo -e "\nApplying migrations in the correct order..."
python manage.py fix_migrate

# Show final migration status
echo -e "\nFinal migration status:"
python manage.py showmigrations

echo -e "\nMigration fix process completed!"
      echo "Unknown option: $1"
      echo "Usage: $0 [--dry-run] [--reset]"
      exit 1
      ;;
  esac
done

# Construct command arguments
ARGS=""
if [ "$DRY_RUN" = true ]; then
  ARGS="$ARGS --dry-run"
fi
if [ "$RESET" = true ]; then
  ARGS="$ARGS --reset"
fi

# Run the fix_migrations management command
echo "Starting migration fix..."
python manage.py fix_migrations $ARGS
