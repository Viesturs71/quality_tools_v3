import os
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import transaction

class Command(BaseCommand):
    help = 'Apply pending migrations in the correct order to resolve dependency issues'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what migrations would be applied without actually applying them'
        )
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Fake-revert pending migrations before applying them'
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        reset = options['reset']
        
        # Order of apps to migrate (resolving dependencies)
        migration_order = [
            'company',        # Apply company migrations first
            'accounts',       # Then accounts which depends on company
            'authentication'  # Then authentication which depends on accounts
        ]
        
        self.stdout.write(self.style.SUCCESS('Starting migration fix...'))
        
        # Show current migration status
        self.stdout.write('Current migration status:')
        call_command('showmigrations')
        
        # First apply company migrations
        for app_name in migration_order:
            if dry_run:
                self.stdout.write(self.style.WARNING(f'Would apply migrations for {app_name}'))
            else:
                try:
                    with transaction.atomic():
                        self.stdout.write(f'Applying migrations for {app_name}...')
                        call_command('migrate', app_name, verbosity=1)
                        self.stdout.write(self.style.SUCCESS(f'Successfully migrated {app_name}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error migrating {app_name}: {str(e)}'))
                    self.stdout.write(self.style.WARNING(
                        f'You might need to manually fix the migration dependencies for {app_name}'
                    ))
        
        # Show final migration status
        if not dry_run:
            self.stdout.write('\nFinal migration status:')
            call_command('showmigrations')
        
        self.stdout.write(self.style.SUCCESS('\nMigration process completed!'))
        
        # Provide guidance for next steps
        if dry_run:
            self.stdout.write('To apply these migrations, run the command without --dry-run')
        else:
            self.stdout.write('If there are still pending migrations, you may need to:')
            self.stdout.write('1. Check migration files for circular dependencies')
            self.stdout.write('2. Try running "python manage.py migrate" to apply all migrations')
            self.stdout.write('3. As a last resort, reset migrations with:')
            self.stdout.write('   - python manage.py migrate app_name zero --fake')
            self.stdout.write('   - Delete migration files (except __init__.py)')
            self.stdout.write('   - python manage.py makemigrations app_name')
            self.stdout.write('   - python manage.py migrate app_name --fake-initial')
        # Show final migration status
        if not dry_run:
            self.stdout.write('\nCurrent migration status:')
            call_command('showmigrations')
        
        self.stdout.write(self.style.SUCCESS('\nMigration process completed!'))
        
        # Provide guidance for next steps
        if dry_run:
            self.stdout.write('To apply these migrations, run the command without --dry-run')
        else:
            self.stdout.write('If there are still pending migrations, you may need to:')
            self.stdout.write('1. Check migration files for circular dependencies')
            self.stdout.write('2. Try the command with --reset to reset the migration state')
            self.stdout.write('3. As a last resort, delete migration files and recreate them')
