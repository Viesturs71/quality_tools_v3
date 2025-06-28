from django.core.management.base import BaseCommand, CommandError
import csv
import os
from django.db import transaction
from apps.personnel.models import Employee
from apps.company.models import Department
from django.utils.translation import gettext as _

class Command(BaseCommand):
    help = 'Import employees from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help='Path to the CSV file')
        parser.add_argument(
            '--update',
            action='store_true',
            help='Update existing employees if they exist'
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
                
                created_count = 0
                updated_count = 0
                skipped_count = 0
                
                with transaction.atomic():
                    for row in reader:
                        employee_id = row.get('employee_id')
                        if not employee_id:
                            self.stderr.write(f"Row missing required employee_id, skipping: {row}")
                            skipped_count += 1
                            continue
                            
                        # Get department if specified
                        department = None
                        department_name = row.get('department')
                        if department_name:
                            try:
                                department = Department.objects.get(name=department_name)
                            except Department.DoesNotExist:
                                if verbose:
                                    self.stdout.write(f"Department {department_name} not found, will be set to None")
                        
                        # Try to find existing employee
                        employee = Employee.objects.filter(employee_id=employee_id).first()
                        
                        # Common fields to set
                        employee_data = {
                            'first_name': row.get('first_name', ''),
                            'last_name': row.get('last_name', ''),
                            'position': row.get('position', ''),
                            'department': department,
                            'email': row.get('email', ''),
                            'phone': row.get('phone', ''),
                            'is_active': row.get('is_active', 'True').lower() == 'true',
                        }
                        
                        # Handle hire date if present
                        if 'hire_date' in row and row['hire_date']:
                            try:
                                employee_data['hire_date'] = row['hire_date']
                            except ValueError:
                                if verbose:
                                    self.stderr.write(f"Invalid date format for hire_date: {row['hire_date']}")
                        
                        if employee:
                            if update_existing:
                                # Update existing employee
                                for key, value in employee_data.items():
                                    setattr(employee, key, value)
                                employee.save()
                                updated_count += 1
                                if verbose:
                                    self.stdout.write(f"Updated: {employee.employee_id} - {employee.first_name} {employee.last_name}")
                            else:
                                skipped_count += 1
                                if verbose:
                                    self.stdout.write(f"Skipped existing: {employee_id}")
                        else:
                            # Create new employee
                            employee_data['employee_id'] = employee_id
                            employee = Employee.objects.create(**employee_data)
                            created_count += 1
                            if verbose:
                                self.stdout.write(f"Created: {employee.employee_id} - {employee.first_name} {employee.last_name}")
                
                self.stdout.write(self.style.SUCCESS(
                    f'Import completed: {created_count} created, {updated_count} updated, {skipped_count} skipped.'
                ))
                
        except Exception as e:
            raise CommandError(f'Error importing employees: {str(e)}')
