import os
import shutil
from pathlib import Path
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.apps import apps


class Command(BaseCommand):
    help = 'Reset migrations for problematic apps and recreate them'

    def add_arguments(self, parser):
        parser.add_argument(
            '--apps',
            nargs='+',
            default=['accounts', 'authentication', 'company', 'equipment'],
            help='Apps to reset migrations for',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without actually making changes',
        )

    def handle(self, *args, **options):
        app_names = options['apps']
        dry_run = options['dry_run']
        
        self.stdout.write(self.style.WARNING('⚠️ This command will reset migrations for specified apps'))
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - no changes will be made'))
        
        for app_name in app_names:
            try:
                app_config = apps.get_app_config(app_name)
                self.stdout.write(f'Processing {app_name}...')
                
                # Step 1: Fake unapply migrations
                if not dry_run:
                    self.stdout.write(f'Fake unapplying migrations for {app_name}...')
                    try:
                        call_command('migrate', app_name, 'zero', '--fake', verbosity=1)
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Error unapplying migrations: {e}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Would fake unapply migrations for {app_name}'))
                
                # Step 2: Remove migration files
                migrations_dir = Path(app_config.path) / 'migrations'
                if migrations_dir.exists():
                    migration_files = [f for f in migrations_dir.iterdir() 
                                     if f.is_file() and f.name != '__init__.py' and f.suffix == '.py']
                    
                    if migration_files:
                        self.stdout.write(f'Found {len(migration_files)} migration files to delete')
                        for f in migration_files:
                            if not dry_run:
                                f.unlink()
                                self.stdout.write(f'Deleted {f.name}')
                            else:
                                self.stdout.write(self.style.WARNING(f'Would delete {f.name}'))
                    else:
                        self.stdout.write('No migration files found')
                
                # Step 3: Create new migrations
                if not dry_run:
                    self.stdout.write(f'Creating new migrations for {app_name}...')
                    try:
                        call_command('makemigrations', app_name, verbosity=1)
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Error creating migrations: {e}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Would create new migrations for {app_name}'))
                
                # Step 4: Fake apply new migrations
                if not dry_run:
                    self.stdout.write(f'Fake applying new migrations for {app_name}...')
                    try:
                        call_command('migrate', app_name, '--fake-initial', verbosity=1)
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Error applying migrations: {e}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Would fake apply migrations for {app_name}'))
                
            except LookupError:
                self.stdout.write(self.style.ERROR(f'App "{app_name}" not found'))
        
        # Final instructions
        if dry_run:
            self.stdout.write(self.style.SUCCESS('Dry run completed. Run without --dry-run to make actual changes'))
        else:
            self.stdout.write(self.style.SUCCESS('Migration reset completed!'))
            self.stdout.write('Run "python manage.py showmigrations" to check the status')
