from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
import csv
import os
from apps.standards.models import Standard, StandardCategory, StandardSection


class Command(BaseCommand):
    help = 'Import standards from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help='Path to the CSV file containing standards data')
        parser.add_argument(
            '--update',
            action='store_true',
            help='Update existing standards if they exist'
        )
        parser.add_argument(
            '--delimiter',
            type=str,
            default=',',
            help='CSV delimiter (default: ,)'
        )

    def handle(self, *args, **options):
        file_path = options['file']
        update_existing = options['update']
        delimiter = options['delimiter']
        
        if not os.path.exists(file_path):
            raise CommandError(f'File not found: {file_path}')
        
        self.stdout.write(f'Importing standards from {file_path}')
        
        try:
            with open(file_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=delimiter)
                
                with transaction.atomic():
                    standards_created = 0
                    standards_updated = 0
                    sections_created = 0
                    
                    for row in reader:
                        # Get or create category
                        category_name = row.get('category', 'General')
                        category, _ = StandardCategory.objects.get_or_create(
                            name=category_name
                        )
                        
                        # Process standard
                        standard_code = row.get('code')
                        standard_name = row.get('name')
                        standard_version = row.get('version', '1.0')
                        
                        if not standard_code or not standard_name:
                            self.stderr.write(f'Skipping row, missing code or name: {row}')
                            continue
                        
                        # Check if standard exists
                        try:
                            standard = Standard.objects.get(
                                code=standard_code,
                                version=standard_version
                            )
                            
                            if update_existing:
                                standard.name = standard_name
                                standard.description = row.get('description', '')
                                standard.category = category
                                standard.save()
                                standards_updated += 1
                                self.stdout.write(f'Updated standard: {standard}')
                            
                        except Standard.DoesNotExist:
                            standard = Standard.objects.create(
                                code=standard_code,
                                name=standard_name,
                                version=standard_version,
                                description=row.get('description', ''),
                                category=category
                            )
                            standards_created += 1
                            self.stdout.write(f'Created standard: {standard}')
                        
                        # Process sections if provided
                        section_number = row.get('section_number')
                        section_name = row.get('section_name')
                        
                        if section_number and section_name:
                            # Check for parent section
                            parent_section = None
                            parent_number = row.get('parent_section')
                            
                            if parent_number:
                                try:
                                    parent_section = StandardSection.objects.get(
                                        standard=standard,
                                        number=parent_number
                                    )
                                except StandardSection.DoesNotExist:
                                    self.stderr.write(f'Parent section {parent_number} not found for {section_number}')
                            
                            # Create or update section
                            section, created = StandardSection.objects.update_or_create(
                                standard=standard,
                                number=section_number,
                                defaults={
                                    'name': section_name,
                                    'description': row.get('section_description', ''),
                                    'content': row.get('section_content', ''),
                                    'parent_section': parent_section,
                                    'order': row.get('section_order', 0)
                                }
                            )
                            
                            if created:
                                sections_created += 1
                                self.stdout.write(f'Created section: {section}')
                    
                    self.stdout.write(self.style.SUCCESS(
                        f'Import completed: {standards_created} standards created, '
                        f'{standards_updated} standards updated, {sections_created} sections created.'
                    ))
                    
        except Exception as e:
            raise CommandError(f'Error importing standards: {str(e)}')
