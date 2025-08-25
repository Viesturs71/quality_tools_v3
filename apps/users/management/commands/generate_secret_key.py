from django.core.management.base import BaseCommand
from django.core.management.utils import get_random_secret_key

class Command(BaseCommand):
    help = 'Generate a new Django secret key'

    def add_arguments(self, parser):
        parser.add_argument(
            '--save-to-env',
            action='store_true',
            help='Save the generated key to .env file',
        )

    def handle(self, *args, **options):
        secret_key = get_random_secret_key()
        
        self.stdout.write(
            self.style.SUCCESS(f'Generated secret key: {secret_key}')
        )
        
        if options['save_to_env']:
            env_file_path = 'c:\\Users\\Viesturs\\anaconda_projects\\quality_tools_v3\\myproject\\.env'
            try:
                # Read existing .env file
                with open(env_file_path, 'r') as f:
                    lines = f.readlines()
                
                # Update or add DJANGO_SECRET_KEY
                key_updated = False
                for i, line in enumerate(lines):
                    if line.startswith('DJANGO_SECRET_KEY='):
                        lines[i] = f'DJANGO_SECRET_KEY={secret_key}\n'
                        key_updated = True
                        break
                
                if not key_updated:
                    lines.append(f'DJANGO_SECRET_KEY={secret_key}\n')
                
                # Write back to file
                with open(env_file_path, 'w') as f:
                    f.writelines(lines)
                
                self.stdout.write(
                    self.style.SUCCESS(f'Secret key saved to {env_file_path}')
                )
                
            except FileNotFoundError:
                self.stdout.write(
                    self.style.ERROR(f'.env file not found at {env_file_path}')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error saving to .env file: {e}')
                )
        else:
            self.stdout.write(
                self.style.WARNING('Add this to your .env file:')
            )
            self.stdout.write(f'DJANGO_SECRET_KEY={secret_key}')
