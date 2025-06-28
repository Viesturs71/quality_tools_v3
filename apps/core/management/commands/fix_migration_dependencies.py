import os
import json
from pathlib import Path
from django.core.management.base import BaseCommand
from django.apps import apps
from django.db import connections


class Command(BaseCommand):
    help = 'Fix migration dependencies issues between apps'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be changed without actually changing anything',
        )
        parser.add_argument(
            '--specific-app',
            type=str,
            help='Fix dependencies only for a specific app',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        specific_app = options.get('specific_app')
        
        # Get all installed Django apps
        django_apps = apps.get_app_configs()
        
        # Filter apps if specific app is provided
        if specific_app:
            django_apps = [app for app in django_apps if app.name.endswith(specific_app)]
            if not django_apps:
                self.stdout.write(self.style.ERROR(f'App "{specific_app}" not found'))
                return
        
        # Get all migration files and their dependencies
        migration_files = {}
        app_dependencies = {}
        
        for app_config in django_apps:
            app_path = Path(app_config.path)
            migrations_dir = app_path / 'migrations'
            
            # Skip if migrations directory doesn't exist
            if not migrations_dir.exists() or not migrations_dir.is_dir():
                continue
            
            app_label = app_config.label
            migration_files[app_label] = []
            
            # Get all migration files
            for file_path in migrations_dir.iterdir():
                if file_path.is_file() and file_path.name.endswith('.py') and file_path.name != '__init__.py':
                    migration_name = file_path.stem
                    migration_files[app_label].append({
                        'name': migration_name,
                        'path': file_path
                    })
        
        # Let's specifically fix the equipment dependency on company
        if 'equipment' in migration_files and 'company' in migration_files:
            self.stdout.write(self.style.SUCCESS("Fixing equipment dependency on company..."))
            
            equipment_initial = None
            company_deps = []
            
            # Find the equipment initial migration
            for migration in migration_files['equipment']:
                if migration['name'] == '0001_initial':
                    equipment_initial = migration
                    break
            
            # Find the company migrations that should be dependencies
            for migration in migration_files['company']:
                if migration['name'] in ['0001_initial', '0002_initial']:
                    company_deps.append(f"('company', '{migration['name']}')")
            
            if equipment_initial and company_deps:
                equipment_path = equipment_initial['path']
                
                # Read the file content
                with open(equipment_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find the dependencies list and add company dependencies if not present
                if 'dependencies = [' in content:
                    # Check if company dependencies are already included
                    missing_deps = []
                    for dep in company_deps:
                        if dep not in content:
                            missing_deps.append(dep)
                    
                    if missing_deps:
                        # Add the missing dependencies
                        modified_content = content.replace(
                            'dependencies = [', 
                            'dependencies = [\n        ' + ',\n        '.join(missing_deps) + ','
                        )
                        
                        if not dry_run:
                            # Backup the original file
                            backup_path = f"{equipment_path}.bak"
                            with open(backup_path, 'w', encoding='utf-8') as f:
                                f.write(content)
                            
                            # Write the modified content
                            with open(equipment_path, 'w', encoding='utf-8') as f:
                                f.write(modified_content)
                            
                            self.stdout.write(self.style.SUCCESS(
                                f"Added company dependencies to equipment/migrations/0001_initial.py"
                            ))
                        else:
                            self.stdout.write(self.style.WARNING(
                                f"Would add these dependencies to equipment/migrations/0001_initial.py: {', '.join(missing_deps)}"
                            ))
                    else:
                        self.stdout.write(self.style.SUCCESS("All necessary dependencies are already included."))
                else:
                    self.stdout.write(self.style.ERROR("Could not find dependencies list in the migration file."))
            else:
                self.stdout.write(self.style.ERROR("Could not find the required migration files."))
        
        self.stdout.write(self.style.SUCCESS(
            "\nNext steps:"
            "\n1. Run 'python manage.py migrate --fake equipment zero' to mark the equipment migrations as unapplied"
            "\n2. Run 'python manage.py migrate company' to apply company migrations"
            "\n3. Run 'python manage.py migrate equipment' to apply equipment migrations with the fixed dependencies"
        ))
