from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Sets up the equipment app by checking and creating necessary database tables'

    def handle(self, *args, **options):
        # Check if the department table exists
        with connection.cursor():
            tables = connection.introspection.table_names()
            if 'equipment_department' not in tables:
                self.stdout.write(self.style.WARNING('Department table not found, running migrations...'))
                # Run migrations
                call_command('makemigrations', 'equipment')
                call_command('migrate', 'equipment')
                self.stdout.write(self.style.SUCCESS('Successfully created department table'))
            else:
                self.stdout.write(self.style.SUCCESS('Department table already exists'))
