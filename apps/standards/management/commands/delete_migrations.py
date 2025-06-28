"""
Management command to delete all migration files except __init__.py
"""
import os
import shutil
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.apps import apps


class Command(BaseCommand):
    help = 'Delete all migration files except __init__.py'

    def add_arguments(self, parser):
        parser.add_argument(
            '--app',
            type=str,
            help='Specific app to delete migrations from (e.g., standards, users)'
        )
        parser.add_argument(
            '--backup',
            action='store_true',
            help='Create backup of migrations before deleting'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting'
        )

    def handle(self, *args, **options):
        app_name = options['app']
        backup = options['backup']
        dry_run = options['dry_run']
        
        # Get base directory for the project
        base_dir = Path(settings.BASE_DIR)
        
        # Get all installed apps that are part of our project
        project_apps = []
        for app_config in apps.get_app_configs():
            if str(app_config.path).startswith(str(base_dir)):
                project_apps.append(app_config)
        
        # Filter to specific app if specified
        if app_name:
            project_apps = [app for app in project_apps if app.name.endswith(app_name)]
            if not project_apps:
                raise CommandError(f'App "{app_name}" not found')
        
        total_deleted = 0
        for app_config in project_apps:
            migrations_dir = Path(app_config.path) / 'migrations'
            if not migrations_dir.exists() or not migrations_dir.is_dir():
                self.stdout.write(self.style.WARNING(f'No migrations directory for {app_config.name}'))
                continue
                
            self.stdout.write(f'Processing migrations for {app_config.name}...')
            
            # Create backup if requested
            if backup and not dry_run:
                backup_dir = f"{migrations_dir}_backup"
                if os.path.exists(backup_dir):
                    shutil.rmtree(backup_dir)
                shutil.copytree(migrations_dir, backup_dir)
                self.stdout.write(self.style.SUCCESS(f'Created backup at {backup_dir}'))
            
            # Find migration files to delete
            migration_files = []
            for file in migrations_dir.iterdir():
                if file.is_file() and file.name != '__init__.py' and file.suffix == '.py':
                    migration_files.append(file)
            
            if not migration_files:
                self.stdout.write(self.style.SUCCESS(f'No migration files to delete in {app_config.name}'))
                continue
            
            self.stdout.write(f'Found {len(migration_files)} migration files in {app_config.name}:')
            for file in migration_files:
                self.stdout.write(f'  - {file.name}')
                
                # Delete the file if not in dry run mode
                if not dry_run:
                    file.unlink()
            
            if not dry_run:
                self.stdout.write(self.style.SUCCESS(f'Deleted {len(migration_files)} migration files from {app_config.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Dry run: Would delete {len(migration_files)} migration files from {app_config.name}'))
            
            total_deleted += len(migration_files)
        
        if not dry_run:
            self.stdout.write(self.style.SUCCESS(f'Total migration files deleted: {total_deleted}'))
            self.stdout.write(self.style.WARNING(
                'Remember to run "python manage.py makemigrations" to create new initial migrations'
            ))
        else:
            self.stdout.write(self.style.SUCCESS(f'Dry run complete. Would delete {total_deleted} migration files.'))
