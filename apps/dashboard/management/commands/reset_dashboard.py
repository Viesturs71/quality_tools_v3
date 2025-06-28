from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.contrib.auth import get_user_model
from apps.dashboard.models import UserPreference, Widget

User = get_user_model()

class Command(BaseCommand):
    help = 'Reset dashboard layouts and widgets for users'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user',
            help='Reset dashboard for a specific user (username)'
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Reset dashboard for all users'
        )
        parser.add_argument(
            '--default-widgets',
            action='store_true',
            help='Add default widgets to reset dashboards'
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Show detailed output'
        )

    def handle(self, *args, **options):
        username = options.get('user')
        reset_all = options.get('all')
        add_defaults = options.get('default_widgets')
        verbose = options.get('verbose')
        
        if not (username or reset_all):
            self.stdout.write(self.style.ERROR('Please specify --user or --all'))
            return
        
        try:
            with transaction.atomic():
                if reset_all:
                    # Reset for all users
                    count = UserPreference.objects.all().count()
                    UserPreference.objects.all().delete()
                    self.stdout.write(self.style.SUCCESS(f'Reset {count} dashboards'))
                    
                    if add_defaults:
                        users = User.objects.all()
                        for user in users:
                            self._add_default_widgets(user, verbose)
                
                elif username:
                    # Reset for specific user
                    try:
                        user = User.objects.get(username=username)
                        UserPreference.objects.filter(user=user).delete()
                        self.stdout.write(self.style.SUCCESS(f'Reset dashboard for user {username}'))
                        
                        if add_defaults:
                            self._add_default_widgets(user, verbose)
                            
                    except User.DoesNotExist:
                        raise CommandError(f'User {username} does not exist')
                
            self.stdout.write(self.style.SUCCESS('Dashboard reset completed!'))
                
        except Exception as e:
            raise CommandError(f'Error resetting dashboard: {str(e)}')
    
    def _add_default_widgets(self, user, verbose):
        """Add default widgets to a user's dashboard"""
        # Create user preference if it doesn't exist
        pref, created = UserPreference.objects.get_or_create(
            user=user,
            defaults={'layout': {'type': 'grid', 'columns': 3}}
        )
        
        # Define default widgets
        default_widgets = [
            {'name': 'Recent Documents', 'type': 'list', 'x': 0, 'y': 0, 'w': 1, 'h': 2},
            {'name': 'Tasks', 'type': 'list', 'x': 1, 'y': 0, 'w': 1, 'h': 1},
            {'name': 'Calendar', 'type': 'calendar', 'x': 2, 'y': 0, 'w': 1, 'h': 2},
            {'name': 'Statistics', 'type': 'stats', 'x': 1, 'y': 1, 'w': 1, 'h': 1},
        ]
        
        # Add default widgets
        for widget_data in default_widgets:
            widget, _ = Widget.objects.get_or_create(
                name=widget_data['name'],
                defaults={
                    'widget_type': widget_data['type'],
                    'description': f'Default {widget_data["name"]} widget',
                    'config': {}
                }
            )
            
            # Link widget to user preference with position
            pref.widget_positions.create(
                widget=widget,
                position_x=widget_data['x'],
                position_y=widget_data['y'],
                width=widget_data['w'],
                height=widget_data['h']
            )
            
            if verbose:
                self.stdout.write(f'Added {widget.name} widget to {user.username}\'s dashboard')
