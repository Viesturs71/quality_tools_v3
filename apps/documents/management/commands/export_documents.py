from django.core.management.base import BaseCommand, CommandError
import csv
import os
from django.utils import timezone
from apps.documents.models import Document

class Command(BaseCommand):
    help = 'Export documents to CSV format'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output', 
            default='documents.csv', 
            help='Output file path'
        )
        parser.add_argument(
            '--status',
            help='Filter by document status (draft, review, approved, published, archived)'
        )
        parser.add_argument(
            '--since',
            help='Documents created since (YYYY-MM-DD)'
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Show detailed output'
        )

    def handle(self, *args, **options):
        output_file = options['output']
        status = options['status']
        since_date = options['since']
        verbose = options['verbose']
        
        try:
            # Build queryset with filters
            queryset = Document.objects.all()
            
            if status:
                queryset = queryset.filter(status=status)
                
            if since_date:
                queryset = queryset.filter(created_at__gte=since_date)
            
            count = queryset.count()
            
            if verbose:
                self.stdout.write(f'Exporting {count} documents to {output_file}')
            
            # Create directory if it doesn't exist
            output_dir = os.path.dirname(output_file)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Export data
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                # Write header
                writer.writerow([
                    'ID', 
                    'Document Number',
                    'Title', 
                    'Type',
                    'Status',
                    'Version',
                    'Created By',
                    'Created At',
                    'Approved By',
                    'Approved At',
                ])
                
                # Write data
                for doc in queryset:
                    writer.writerow([
                        doc.id,
                        doc.document_number,
                        doc.title,
                        doc.get_document_type_display(),
                        doc.get_status_display(),
                        doc.version,
                        doc.created_by.username if doc.created_by else '',
                        doc.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                        doc.approved_by.username if doc.approved_by else '',
                        doc.approved_at.strftime('%Y-%m-%d %H:%M:%S') if doc.approved_at else '',
                    ])
            
            self.stdout.write(self.style.SUCCESS(f'Successfully exported {count} documents to {output_file}'))
            
        except Exception as e:
            raise CommandError(f'Error exporting documents: {str(e)}')
