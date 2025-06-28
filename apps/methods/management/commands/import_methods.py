from django.core.management.base import BaseCommand, CommandError
import csv
import os
from django.utils import timezone
from django.db import transaction
from apps.methods.models import Method


class Command(BaseCommand):
    help = 'Import methods from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help='Path to the CSV file')
        parser.add_argument(
            '--update',
            action='store_true',
            help='Update existing methods if they exist'
        )
        parser.add_argument(
            '--delimiter',
            type=str,
            default=',',
            help='CSV delimiter (default: ,)'
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Show detailed output'
        )

    def handle(self, *args, **options):
        file_path = options['file']
        update_existing = options['update']
        delimiter = options['delimiter']
        verbose = options['verbose']
        
        if not os.path.exists(file_path):
            raise CommandError(f'File not found: {file_path}')
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter=delimiter)
                
                if verbose:
                    self.stdout.write(f"Starting import from {file_path}")
                
                methods_created = 0
                methods_updated = 0
                methods_skipped = 0
                
                with transaction.atomic():
                    for row in reader:
                        identification = row.get('identification')
                        if not identification:
                            self.stderr.write(f"Row missing required identification, skipping: {row}")
                            methods_skipped += 1
                            continue
                            
                        # Try to find existing method
                        method = Method.objects.filter(identification=identification).first()
                        
                        # Common fields to set
                        method_data = {
                            'name': row.get('name', ''),
                            'investigation_field': row.get('investigation_field', ''),
                            'analyzer': row.get('analyzer', ''),
                            'technology': row.get('technology', ''),
                            'test_material': row.get('test_material', ''),
                            'location': row.get('location', ''),
                        }
                        
                        # Handle verification date if present
                        if 'verification_date' in row and row['verification_date']:
                            try:
                                method_data['verification_date'] = row['verification_date']
                            except ValueError:
                                if verbose:
                                    self.stderr.write(f"Invalid date format: {row['verification_date']}")
                        
                        if method:
                            if update_existing:
                                # Update existing method
                                for key, value in method_data.items():
                                    setattr(method, key, value)
                                method.save()
                                methods_updated += 1
                                if verbose:
                                    self.stdout.write(f"Updated: {method.identification} - {method.name}")
                            else:
                                methods_skipped += 1
                                if verbose:
                                    self.stdout.write(f"Skipped existing: {identification}")
                        else:
                            # Create new method
                            method_data['identification'] = identification
                            method = Method.objects.create(**method_data)
                            methods_created += 1
                            if verbose:
                                self.stdout.write(f"Created: {method.identification} - {method.name}")
                
                self.stdout.write(self.style.SUCCESS(
                    f'Import completed: {methods_created} created, {methods_updated} updated, {methods_skipped} skipped.'
                ))
                
        except Exception as e:
            raise CommandError(f'Error importing methods: {str(e)}')
