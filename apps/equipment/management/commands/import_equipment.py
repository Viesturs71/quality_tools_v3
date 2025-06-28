from django.core.management.base import BaseCommand, CommandError
import csv
from django.db import transaction
from apps.equipment.models import Equipment, EquipmentType, EquipmentCategory


class Command(BaseCommand):
    help = 'Import equipment from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file', help='CSV file path')
        parser.add_argument('--update', action='store_true', help='Update existing records')
        parser.add_argument('--delimiter', default=',', help='CSV delimiter character')
        parser.add_argument('--verbose', action='store_true', help='Show detailed output')

    def handle(self, *args, **options):
        file_path = options['file']
        update = options['update']
        delimiter = options['delimiter']
        verbose = options['verbose']
        
        try:
            with open(file_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=delimiter)
                
                created = 0
                updated = 0
                skipped = 0
                
                with transaction.atomic():
                    for row in reader:
                        # Find or create equipment type
                        equipment_type, _ = EquipmentType.objects.get_or_create(
                            name=row.get('type', 'Unknown'),
                            defaults={'description': f"Imported from CSV: {row.get('type', 'Unknown')}"}
                        )
                        
                        # Find or create category if specified
                        category = None
                        if 'category' in row and row['category']:
                            category, _ = EquipmentCategory.objects.get_or_create(
                                name=row['category']
                            )
                        
                        # Look for existing equipment by inventory number
                        inventory_number = row.get('inventory_number', '')
                        if not inventory_number:
                            self.stderr.write(f"Row missing required inventory_number, skipping: {row}")
                            skipped += 1
                            continue
                            
                        equipment = Equipment.objects.filter(
                            inventory_number=inventory_number
                        ).first()
                        
                        # Common fields to set
                        equipment_data = {
                            'name': row.get('name', ''),
                            'equipment_type': equipment_type,
                            'description': row.get('description', ''),
                            'manufacturer': row.get('manufacturer', ''),
                            'model_number': row.get('model_number', ''),
                            'serial_number': row.get('serial_number', ''),
                            'status': row.get('status', 'active'),
                        }
                        
                        # Handle purchase date if present and valid
                        if 'purchase_date' in row and row['purchase_date']:
                            try:
                                equipment_data['purchase_date'] = row['purchase_date']
                            except ValueError:
                                if verbose:
                                    self.stderr.write(f"Invalid purchase date format: {row['purchase_date']}")
                        
                        if equipment:
                            if update:
                                # Update existing equipment
                                for key, value in equipment_data.items():
                                    setattr(equipment, key, value)
                                equipment.save()
                                updated += 1
                                if verbose:
                                    self.stdout.write(f"Updated: {equipment.inventory_number} - {equipment.name}")
                            else:
                                skipped += 1
                                if verbose:
                                    self.stdout.write(f"Skipped existing: {inventory_number}")
                        else:
                            # Create new equipment
                            equipment_data['inventory_number'] = inventory_number
                            equipment = Equipment.objects.create(**equipment_data)
                            created += 1
                            if verbose:
                                self.stdout.write(f"Created: {equipment.inventory_number} - {equipment.name}")
                
                self.stdout.write(self.style.SUCCESS(
                    f'Import completed: {created} created, {updated} updated, {skipped} skipped.'
                ))
                
        except FileNotFoundError:
            raise CommandError(f'File {file_path} not found')
        except Exception as e:
            raise CommandError(f'Error importing data: {str(e)}')
