import os
import shutil
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
from django.apps import apps


class Command(BaseCommand):
    help = 'Delete all migration files from all apps except __init__.py'

    def add_arguments(self, parser):
        parser.add_argument(
            '--backup',
            action='store_true',
            help='Create backup of migrations before deleting',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting',
        )
        parser.add_argument(
            '--specific-app',
            type=str,
            help='Delete migrations only for a specific app',
        )

    def handle(self, *args, **options):
        backup = options['backup']
        dry_run = options['dry_run']
        specific_app = options.get('specific_app')
        
        # Get all installed Django apps
        django_apps = apps.get_app_configs()
        total_deleted = 0
        
        # Filter apps if specific app is provided
        if specific_app:
            django_apps = [app for app in django_apps if app.name.endswith(specific_app)]
            if not django_apps:
                self.stdout.write(self.style.ERROR(f'App "{specific_app}" not found'))
                return
        
        for app_config in django_apps:
            app_path = Path(app_config.path)
            migrations_dir = app_path / 'migrations'
            
            # Skip if migrations directory doesn't exist
            if not migrations_dir.exists() or not migrations_dir.is_dir():
                continue
                
            self.stdout.write(f'Processing migrations for {app_config.label}...')
            
            # Create backup if requested
            if backup and not dry_run:
                backup_dir = f"{migrations_dir}_backup_{self._get_timestamp()}"
                if os.path.exists(backup_dir):
                    shutil.rmtree(backup_dir)
                shutil.copytree(migrations_dir, backup_dir)
                self.stdout.write(self.style.SUCCESS(f'Created backup at {backup_dir}'))
            
            # Get all migration files except __init__.py
            migration_files = []
            for file_path in migrations_dir.iterdir():
                if file_path.is_file() and file_path.name != '__init__.py' and file_path.suffix == '.py':
                    migration_files.append(file_path)
            
            if not migration_files:
                self.stdout.write(self.style.SUCCESS(f'No migration files to delete in {app_config.label}'))
                continue
            
            # Report files to be deleted
            self.stdout.write(f'Found {len(migration_files)} migration files in {app_config.label}:')
            for file_path in migration_files:
                self.stdout.write(f'  - {file_path.name}')
                
                # Delete the file if not in dry run mode
                if not dry_run:
                    file_path.unlink()
            
            # Report results
            if not dry_run:
                self.stdout.write(self.style.SUCCESS(
                    f'Deleted {len(migration_files)} migration files from {app_config.label}'
                ))
            else:
                self.stdout.write(self.style.WARNING(
                    f'Dry run: Would delete {len(migration_files)} migration files from {app_config.label}'
                ))
            
            total_deleted += len(migration_files)
        
        # Final summary
        if total_deleted == 0:
            self.stdout.write(self.style.SUCCESS('No migration files found to delete'))
        elif dry_run:
            self.stdout.write(self.style.SUCCESS(f'Dry run completed. Would delete {total_deleted} migration files'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Successfully deleted {total_deleted} migration files'))
            self.stdout.write(self.style.WARNING(
                'Remember to run "python manage.py makemigrations" to create new initial migrations'
            ))
    
    def _get_timestamp(self):
        """Generate a timestamp string for backup directory names."""
        from datetime import datetime
        return datetime.now().strftime('%Y%m%d_%H%M%S')
