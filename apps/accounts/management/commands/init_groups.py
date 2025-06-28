from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

# Use proper import paths with apps prefix
from apps.standards.models import Standard
from apps.personnel.models import Employee
from apps.documents.models import QualityDocument

class Command(BaseCommand):
    help = 'Initializes default user groups and permissions'

    def add_arguments(self, parser):
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Display detailed output',
        )

    def handle(self, *args, **options):
        verbose = options.get('verbose', False)
        
        groups = {
            "Doc Admins": {
                "permissions": [
                    "add_qualitydocument", "change_qualitydocument", "delete_qualitydocument", "view_qualitydocument"
                ]
            },
            "Standards Viewers": {
                "permissions": ["view_standard"]
            },
            "Personnel Admins": {
                "permissions": [
                    "add_employee", "change_employee", "delete_employee", "view_employee"
                ]
            }
        }

        for group_name, data in groups.items():
            if verbose:
                self.stdout.write(f"Processing group: {group_name}")
                
            group, created = Group.objects.get_or_create(name=group_name)
            
            if created and verbose:
                self.stdout.write(self.style.SUCCESS(f"Created group: {group_name}"))
            
            for perm_codename in data["permissions"]:
                try:
                    perm = Permission.objects.get(codename=perm_codename)
                    group.permissions.add(perm)
                    if verbose:
                        self.stdout.write(f"Added permission: {perm_codename}")
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Permission not found: {perm_codename}"))
            
            self.stdout.write(self.style.SUCCESS(f"Group '{group_name}' initialized with permissions."))

        self.stdout.write(self.style.SUCCESS("All groups and permissions initialized."))
