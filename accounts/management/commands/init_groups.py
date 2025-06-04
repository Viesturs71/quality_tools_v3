from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from quality_docs.models import QualityDocument
from personnel.models import Employee
from standards.models import Standard

class Command(BaseCommand):
    help = 'Initializes default user groups and permissions'

    def handle(self, *args, **options):
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
            group, created = Group.objects.get_or_create(name=group_name)
            for perm_codename in data["permissions"]:
                try:
                    perm = Permission.objects.get(codename=perm_codename)
                    group.permissions.add(perm)
                except Permission.DoesNotExist:
                    self.stdout.write(f"Permission not found: {perm_codename}")
            self.stdout.write(f"Group '{group_name}' initialized with permissions.")

        self.stdout.write("All groups and permissions initialized.")
