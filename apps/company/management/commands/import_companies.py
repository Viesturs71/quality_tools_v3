from django.core.management.base import BaseCommand, CommandError
import csv
import os
from django.db import transaction
from apps.company.models import Company, Location


class Command(BaseCommand):
    help = 'Import companies and locations from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help='Path to the CSV file')
        parser.add_argument(
            '--update',
            action='store_true',
            help='Update existing companies'
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
                
                companies_created = 0
                companies_updated = 0
                locations_created = 0
                
                with transaction.atomic():
                    for row in reader:
                        # Process company
                        company, company_created = self._process_company(row, update_existing)
                        
                        if company_created:
                            companies_created += 1
                            if verbose:
                                self.stdout.write(f"Created company: {company.name}")
                        elif update_existing:
                            companies_updated += 1
                            if verbose:
                                self.stdout.write(f"Updated company: {company.name}")
                        
                        # Process location if address is provided
                        if row.get('address'):
                            location, location_created = self._process_location(row, company)
                            if location_created:
                                locations_created += 1
                                if verbose:
                                    self.stdout.write(f"Created location for {company.name}: {location.name}")
                
                self.stdout.write(self.style.SUCCESS(
                    f"Import completed: {companies_created} companies created, "
                    f"{companies_updated} companies updated, "
                    f"{locations_created} locations created."
                ))
                
        except Exception as e:
            raise CommandError(f"Error importing companies: {str(e)}")
    
    def _process_company(self, row, update_existing):
        """Process a company from a CSV row."""
        identifier = row.get('identifier')
        name = row.get('name')
        
        if not identifier or not name:
            raise CommandError("CSV row missing required fields: identifier, name")
        
        # Try to find existing company
        company = Company.objects.filter(identifier=identifier).first()
        created = False
        
        if company:
            if update_existing:
                # Update existing company
                company.name = name
                company.registration_number = row.get('registration_number', '')
                company.phone = row.get('phone', '')
                company.email = row.get('email', '')
                company.is_active = row.get('is_active', 'True').lower() == 'true'
                company.save()
        else:
            # Create new company
            company = Company.objects.create(
                identifier=identifier,
                name=name,
                registration_number=row.get('registration_number', ''),
                address=row.get('address', ''),
                phone=row.get('phone', ''),
                email=row.get('email', ''),
                is_active=row.get('is_active', 'True').lower() == 'true'
            )
            created = True
        
        return company, created
    
    def _process_location(self, row, company):
        """Process a location from a CSV row."""
        location_name = row.get('location_name', company.name)
        address = row.get('address', '')
        
        # Check if location already exists
        location = Location.objects.filter(
            company=company,
            name=location_name,
            address=address
        ).first()
        
        if location:
            return location, False
        
        # Create new location
        location = Location.objects.create(
            company=company,
            name=location_name,
            address=address,
            is_active=True
        )
        
        return location, True
