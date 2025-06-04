import os
import shutil
import datetime
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.apps import apps

class Command(BaseCommand):
    help = 'Reset migrations for specified Django apps or all apps'

    def add_arguments(self, parser):
        parser.add_argument(
            'apps', nargs='*', type=str,
            help='List of app names to reset migrations for (empty for all apps)'
        )
        parser.add_argument(
            '--no-backup', action='store_true', dest='no_backup',
            help='Do not backup migrations before deleting'
        )
        parser.add_argument(
            '--check', action='store_true', dest='check_only',
            help='Only check the status of migrations without making changes'
        )

    def handle(self, *args, **options):
        app_labels = options['apps']
        backup = not options['no_backup']
        check_only = options['check_only']
        
        if check_only:
            self.check_migrations_status()
            return
            
        if not app_labels:
            # If no apps specified, get all installed apps
            app_labels = [app_config.label for app_config in apps.get_app_configs()]
            
        # Confirm with the user before proceeding
        if not options.get('no_input', False):
            confirm = input(f"Are you sure you want to reset migrations for {', '.join(app_labels)}? [y/N]: ")
            if confirm.lower() != 'y':
                self.stdout.write(self.style.WARNING('Operation cancelled.'))
                return
        
        # Create backup directory if needed
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        if backup:
            backup_dir = os.path.join(settings.BASE_DIR, f'migrations_backup_{timestamp}')
            os.makedirs(backup_dir, exist_ok=True)
            self.stdout.write(f"Created backup directory: {backup_dir}")
        
        # Process each app
        for app_label in app_labels:
            try:
                app_config = apps.get_app_config(app_label)
                migrations_dir = os.path.join(app_config.path, 'migrations')
                
                if not os.path.isdir(migrations_dir):
                    self.stdout.write(self.style.WARNING(f"No migrations directory found for {app_label}"))
                    continue
                
                # Process migration files
                migration_files = [f for f in os.listdir(migrations_dir) 
                                  if f.endswith('.py') and f != '__init__.py']
                
                # Backup migrations if enabled
                if backup and migration_files:
                    app_backup_dir = os.path.join(backup_dir, app_label, 'migrations')
                    os.makedirs(app_backup_dir, exist_ok=True)
                    
                    for file in migration_files:
                        src_path = os.path.join(migrations_dir, file)
                        dst_path = os.path.join(app_backup_dir, file)
                        shutil.copy2(src_path, dst_path)
                        self.stdout.write(f"Backed up: {src_path}")
                
                # Delete migration files
                for file in migration_files:
                    file_path = os.path.join(migrations_dir, file)
                    os.remove(file_path)
                    self.stdout.write(self.style.SUCCESS(f"Deleted: {file_path}"))
                
                # Ensure __init__.py exists
                init_path = os.path.join(migrations_dir, '__init__.py')
                if not os.path.exists(init_path):
                    with open(init_path, 'w') as f:
                        pass
                    self.stdout.write(f"Created missing __init__.py in: {migrations_dir}")
                
                self.stdout.write(self.style.SUCCESS(f"Successfully reset migrations for {app_label}"))
            
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error processing {app_label}: {str(e)}"))
        
        self.stdout.write(self.style.SUCCESS("\nMigration reset completed."))
        self.stdout.write("Remember to run 'python manage.py makemigrations' to create new initial migrations.")

    def check_migrations_status(self):
        """Check and display the status of migrations for all apps."""
        self.stdout.write("\nChecking migrations status...\n")
        
        app_stats = {}
        
        for app_config in apps.get_app_configs():
            migrations_dir = os.path.join(app_config.path, 'migrations')
            
            if not os.path.isdir(migrations_dir):
                continue
                
            migration_files = [f for f in os.listdir(migrations_dir) 
                              if f.endswith('.py') and f != '__init__.py']
            
            # Check if __init__.py exists
            has_init = os.path.exists(os.path.join(migrations_dir, '__init__.py'))
            
            app_stats[app_config.label] = {
                'count': len(migration_files),
                'has_init': has_init,
                'path': migrations_dir
            }
        
        # Print results in a sorted manner
        for app_label in sorted(app_stats.keys()):
            stats = app_stats[app_label]
            status = self.style.SUCCESS("OK") if stats['has_init'] else self.style.ERROR("Missing __init__.py")
            self.stdout.write(f"{app_label}: {stats['count']} migration(s) - {status}")
        
        # Calculate totals
        total_migrations = sum(stats['count'] for stats in app_stats.values())
        total_apps = len(app_stats)
        init_missing = sum(1 for stats in app_stats.values() if not stats['has_init'])
        
        self.stdout.write(f"\nTotal: {total_migrations} migration files across {total_apps} apps")
        if init_missing > 0:
            self.stdout.write(self.style.WARNING(f"Warning: {init_missing} migrations directories missing __init__.py"))
