from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.authentication.models import Token


class Command(BaseCommand):
    help = 'Clean up expired authentication tokens'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting it',
        )
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Delete tokens older than this many days (default: 30)',
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Show detailed output',
        )

    def handle(self, *args, **options):
        days = options['days']
        dry_run = options['dry_run']
        verbose = options['verbose']
        
        cutoff_date = timezone.now() - timezone.timedelta(days=days)
        
        # Find expired tokens
        expired_tokens = Token.objects.filter(
            created__lt=cutoff_date
        )
        
        # Find explicitly expired tokens
        explicitly_expired = Token.objects.filter(
            expires__lt=timezone.now()
        )
        
        # Combine and remove duplicates
        tokens_to_delete = expired_tokens | explicitly_expired
        count = tokens_to_delete.count()
        
        if verbose:
            self.stdout.write(f"Found {count} expired tokens to clean up")
        
        if dry_run:
            self.stdout.write(self.style.WARNING(f"Would delete {count} tokens (dry run)"))
            if verbose and count > 0:
                for token in tokens_to_delete:
                    self.stdout.write(f"  - Token {token.key[:10]}... for user {token.user.username}")
        else:
            if count > 0:
                tokens_to_delete.delete()
                self.stdout.write(self.style.SUCCESS(f"Successfully deleted {count} expired tokens"))
            else:
                self.stdout.write("No expired tokens found")
