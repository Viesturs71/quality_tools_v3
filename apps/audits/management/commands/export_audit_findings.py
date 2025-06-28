from django.core.management.base import BaseCommand, CommandError
import csv
import os
from django.utils import timezone
from apps.audits.models import Audit, AuditFinding


class Command(BaseCommand):
    help = 'Export audit findings to CSV format'

    def add_arguments(self, parser):
        parser.add_argument('--output', default='audit_findings.csv', help='Output file path')
        parser.add_argument('--audit', type=int, help='Specific audit ID to export')
        parser.add_argument('--severity', help='Filter by severity (critical, major, minor, observation)')
        parser.add_argument('--verbose', action='store_true', help='Verbose output')

    def handle(self, *args, **options):
        output_file = options['output']
        audit_id = options['audit']
        severity = options['severity']
        verbose = options['verbose']
        
        try:
            # Build queryset with filters
            queryset = AuditFinding.objects.all().select_related('audit')
            
            if audit_id:
                queryset = queryset.filter(audit_id=audit_id)
                
            if severity:
                queryset = queryset.filter(severity=severity)
            
            count = queryset.count()
            
            if verbose:
                self.stdout.write(f'Exporting {count} audit findings to {output_file}')
            
            # Create directory if it doesn't exist
            output_dir = os.path.dirname(output_file)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Export data
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                # Write header
                writer.writerow([
                    'Audit Title', 
                    'Audit Date', 
                    'Finding Description', 
                    'Severity', 
                    'Reference',
                    'Created At'
                ])
                
                # Write data
                for finding in queryset:
                    writer.writerow([
                        finding.audit.title,
                        finding.audit.date.strftime('%Y-%m-%d'),
                        finding.description,
                        finding.get_severity_display(),
                        finding.reference,
                        finding.created_at.strftime('%Y-%m-%d %H:%M:%S')
                    ])
            
            self.stdout.write(self.style.SUCCESS(f'Successfully exported {count} findings to {output_file}'))
            
        except Exception as e:
            raise CommandError(f'Error exporting audit findings: {str(e)}')
