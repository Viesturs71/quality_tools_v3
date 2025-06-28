from django.core.management.base import BaseCommand
from django.urls import get_resolver
import sys


class Command(BaseCommand):
    help = 'Displays all available URL patterns in the project'

    def add_arguments(self, parser):
        parser.add_argument(
            '--filter',
            dest='filter',
            help='Filter URLs by name (case-insensitive)',
        )
        parser.add_argument(
            '--format',
            choices=['text', 'json'],
            default='text',
            help='Output format (default: text)',
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Show detailed URL information',
        )

    def handle(self, *args, **options):
        url_filter = options.get('filter', '').lower()
        output_format = options.get('format')
        verbose = options.get('verbose')
        
        resolver = get_resolver()
        
        # Get all URL patterns
        url_patterns = []
        
        def extract_urls(patterns, namespace=None, path_prefix=''):
            for pattern in patterns:
                pattern_name = getattr(pattern, 'name', None)
                pattern_namespace = namespace
                
                if hasattr(pattern, 'url_patterns'):
                    # This is an include or a namespaced URL
                    if hasattr(pattern, 'namespace') and pattern.namespace:
                        pattern_namespace = pattern.namespace
                        
                    if hasattr(pattern, 'pattern'):
                        prefix = path_prefix + str(pattern.pattern)
                    else:
                        prefix = path_prefix
                        
                    extract_urls(pattern.url_patterns, pattern_namespace, prefix)
                    continue
                
                # Get the full URL name with namespace
                if pattern_namespace and pattern_name:
                    full_name = f"{pattern_namespace}:{pattern_name}"
                else:
                    full_name = pattern_name
                
                # Skip if filtering and name doesn't match
                if url_filter and (not full_name or url_filter not in full_name.lower()):
                    continue
                
                # Get the URL pattern
                url = path_prefix
                if hasattr(pattern, 'pattern'):
                    url += str(pattern.pattern)
                
                # Add to the list
                url_patterns.append({
                    'name': full_name,
                    'pattern': url,
                    'view': str(pattern.callback.__module__ + '.' + pattern.callback.__name__) if callable(getattr(pattern, 'callback', None)) else str(pattern.callback)
                })
        
        # Extract all URLs
        extract_urls(resolver.url_patterns)
        
        # Sort by name
        url_patterns.sort(key=lambda x: (x['name'] or '', x['pattern']))
        
        # Output the results
        if output_format == 'json':
            import json
            self.stdout.write(json.dumps(url_patterns, indent=2))
        else:
            # Text format
            self.stdout.write(self.style.SUCCESS(f"Found {len(url_patterns)} URL patterns:"))
            self.stdout.write("")
            
            if not url_patterns:
                self.stdout.write(self.style.WARNING("No URLs found matching your criteria."))
                return
            
            name_width = max(len(p['name'] or '') for p in url_patterns) + 2
            
            for pattern in url_patterns:
                name = pattern['name'] or '(No name)'
                self.stdout.write(f"{name:{name_width}} {pattern['pattern']}")
                
                if verbose:
                    self.stdout.write(f"{'':>{name_width}} View: {pattern['view']}")
                    self.stdout.write("")
