from django.core.management.base import BaseCommand, CommandError
import csv
import os
from django.db import transaction
from django.contrib.auth import get_user_model
from apps.users.models import Profile

User = get_user_model()

class Command(BaseCommand):
    help = 'Import users from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help='Path to the CSV file')
        parser.add_argument(
            '--update',
            action='store_true',
            help='Update existing users if they exist'
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
                
                users_created = 0
                users_updated = 0
                users_skipped = 0
                
                with transaction.atomic():
                    for row in reader:
                        username = row.get('username')
                        email = row.get('email')
                        
                        if not username or not email:
                            self.stderr.write(f"Row missing required username or email, skipping: {row}")
                            users_skipped += 1
                            continue
                            
                        # Try to find existing user
                        user = User.objects.filter(username=username).first()
                        
                        if user:
                            if update_existing:
                                # Update existing user
                                user.email = email
                                user.first_name = row.get('first_name', '')
                                user.last_name = row.get('last_name', '')
                                
                                if row.get('password'):
                                    user.set_password(row.get('password'))
                                
                                user.save()
                                
                                # Update profile
                                profile = getattr(user, 'profile', None)
                                if profile:
                                    profile.department = row.get('department', '')
                                    profile.position = row.get('position', '')
                                    profile.phone = row.get('phone', '')
                                    profile.bio = row.get('bio', '')
                                    profile.save()
                                
                                users_updated += 1
                                if verbose:
                                    self.stdout.write(f"Updated: {user.username} - {user.email}")
                            else:
                                users_skipped += 1
                                if verbose:
                                    self.stdout.write(f"Skipped existing: {username}")
                        else:
                            # Create new user
                            user = User.objects.create_user(
                                username=username,
                                email=email,
                                password=row.get('password', 'changeme'),
                                first_name=row.get('first_name', ''),
                                last_name=row.get('last_name', '')
                            )
                            
                            # Update profile
                            profile = getattr(user, 'profile', None)
                            if profile:
                                profile.department = row.get('department', '')
                                profile.position = row.get('position', '')
                                profile.phone = row.get('phone', '')
                                profile.bio = row.get('bio', '')
                                profile.save()
                            
                            users_created += 1
                            if verbose:
                                self.stdout.write(f"Created: {user.username} - {user.email}")
                
                self.stdout.write(self.style.SUCCESS(
                    f'Import completed: {users_created} created, {users_updated} updated, {users_skipped} skipped.'
                ))
                
        except Exception as e:
            raise CommandError(f'Error importing users: {str(e)}')
