from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connections, transaction
from django.db.migrations.recorder import MigrationRecorder
from django.utils import timezone
import datetime

class Command(BaseCommand):
    help = 'Fix migration dependencies and apply migrations in the correct order'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be applied without actually applying'
        )
        parser.add_argument(
            '--force-reorder',
            action='store_true',
            help='Force reordering of migrations even if no issues are detected'
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        force_reorder = options['force_reorder']
        
        self.stdout.write(self.style.SUCCESS('Starting migration fix process...'))
        
        # First check if we need to fix the migration history
        connection = connections['default']
        recorder = MigrationRecorder(connection)
        
        # Get problematic migration records
        company_0002 = recorder.migration_qs.filter(app='company', name='0002_initial').first()
        equipment_0001 = recorder.migration_qs.filter(app='equipment', name='0001_initial').first()
        
        # Display current state
        if company_0002 and equipment_0001:
            self.stdout.write("Current migration timestamps:")
            self.stdout.write(f"  company.0002_initial: {company_0002.applied}")
            self.stdout.write(f"  equipment.0001_initial: {equipment_0001.applied}")
            
            # Check if equipment migration is applied before its company dependency
            needs_fixing = equipment_0001.applied < company_0002.applied
            
            if needs_fixing or force_reorder:
                self.stdout.write(self.style.WARNING('Found inconsistent migration history. Fixing...'))
                
                if not dry_run:
                    # Fix the migration history - set equipment migration to be after company
                    new_time = company_0002.applied + datetime.timedelta(seconds=1)
                    self.stdout.write(f"  Setting equipment.0001_initial timestamp to: {new_time}")
                    
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "UPDATE django_migrations SET applied = %s WHERE app = %s AND name = %s",
                            [new_time, 'equipment', '0001_initial']
                        )
                    self.stdout.write(self.style.SUCCESS('Migration history fixed!'))
                else:
                    self.stdout.write(self.style.WARNING('Would fix migration history (dry run)'))
        
        # Migration order to ensure proper dependencies
        migration_sequence = [
            'company',       # Base company structure
            'personnel',     # Personnel models
            'equipment',     # Equipment models
            'accounts',      # Accounts which may depend on company
            'authentication' # Authentication which may depend on accounts
        ]
        
        # Show current migration status
        if not dry_run:
            self.stdout.write('\nCurrent migration status before applying fixes:')
            call_command('showmigrations')
        
        # Apply migrations in the correct order
        for app_name in migration_sequence:
            if dry_run:
                self.stdout.write(self.style.WARNING(f'Would migrate: {app_name}'))
            else:
                try:
                    self.stdout.write(f'Migrating {app_name}...')
                    call_command('migrate', app_name, verbosity=1)
                    self.stdout.write(self.style.SUCCESS(f'Successfully migrated {app_name}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error migrating {app_name}: {str(e)}'))
                    self.stdout.write(self.style.WARNING(
                        f'Migration process stopped. You might need to fix {app_name} migrations manually.'
                    ))
                    return
        
        # Show final migration status
        if not dry_run:
            self.stdout.write('\nFinal migration status:')
            call_command('showmigrations')
        
        self.stdout.write(self.style.SUCCESS('\nMigration process completed successfully!'))
        
        if dry_run:
            self.stdout.write(self.style.WARNING('\nThis was a dry run. To apply changes, run without --dry-run'))
        else:
            self.stdout.write('\nYou should now be able to make new migrations with:')
            self.stdout.write('  python manage.py makemigrations')
