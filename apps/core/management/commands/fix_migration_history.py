from django.core.management.base import BaseCommand
from django.db import connections
from django.db.migrations.recorder import MigrationRecorder
from django.conf import settings
import datetime

class Command(BaseCommand):
    help = 'Fix inconsistent migration history by correcting migration application dates'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what changes would be made without actually applying them'
        )
        parser.add_argument(
            '--database',
            default='default',
            help='Database to use (default: "default")'
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        database = options['database']
        
        self.stdout.write(self.style.NOTICE('Analyzing migration history...'))
        
        # Get connection and migration recorder
        connection = connections[database]
        recorder = MigrationRecorder(connection)
        migration_records = list(recorder.migration_qs.all())
        
        # Find problematic migrations
        company_0002 = None
        equipment_0001 = None
        
        for record in migration_records:
            if record.app == 'company' and record.name == '0002_initial':
                company_0002 = record
            elif record.app == 'equipment' and record.name == '0001_initial':
                equipment_0001 = record
        
        if not company_0002 or not equipment_0001:
            self.stdout.write(self.style.ERROR('Could not find one or both migrations mentioned in the error.'))
            return
        
        # Show current state
        self.stdout.write(f'Current state:')
        self.stdout.write(f'  equipment.0001_initial: Applied at {equipment_0001.applied}')
        self.stdout.write(f'  company.0002_initial: Applied at {company_0002.applied}')
        
        # Check if there's an issue to fix
        if equipment_0001.applied > company_0002.applied:
            self.stdout.write(self.style.SUCCESS('No fix needed: equipment.0001_initial is already after company.0002_initial'))
            return
        
        # Prepare the fix
        new_equipment_date = company_0002.applied + datetime.timedelta(seconds=1)
        
        self.stdout.write(self.style.WARNING(f'\nWill update equipment.0001_initial application date:'))
        self.stdout.write(f'  From: {equipment_0001.applied}')
        self.stdout.write(f'  To:   {new_equipment_date} (1 second after company.0002_initial)')
        
        if dry_run:
            self.stdout.write(self.style.WARNING('\nDRY RUN: No changes made.'))
            self.stdout.write('To apply these changes, run without --dry-run.')
            return
        
        # Apply the fix
        self.stdout.write(self.style.WARNING('\nApplying fix...'))
        
        with connection.cursor() as cursor:
            # Update the applied date of equipment.0001_initial to be after company.0002_initial
            cursor.execute(
                "UPDATE django_migrations SET applied = %s WHERE app = %s AND name = %s",
                [new_equipment_date, "equipment", "0001_initial"]
            )
        
        self.stdout.write(self.style.SUCCESS('\nMigration history has been fixed!'))
        self.stdout.write('You can now run migrations normally.')
        
        # Verify the fix worked
        updated_record = recorder.migration_qs.get(app='equipment', name='0001_initial')
        self.stdout.write(f'\nVerification:')
        self.stdout.write(f'  equipment.0001_initial: Now applied at {updated_record.applied}')
