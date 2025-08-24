from django.db.models import Count, Case, When, IntegerField, Q
from .models import StandardDocumentLink, StandardSection
from apps.documents.models import Document

def check_document_compliance(document_id):
    """
    Check compliance status for a specific document across all linked standards.
    Returns detailed compliance information.
    """
    try:
        document = Document.objects.get(id=document_id)
        links = StandardDocumentLink.objects.filter(document=document)
        
        compliance_data = {
            'document': document,
            'total_links': links.count(),
            'compliance_breakdown': {},
            'overall_compliance_percentage': 0,
            'links': []
        }
        
        # Count by status
        status_counts = links.aggregate(
            compliant=Count(Case(When(compliance_status='compliant', then=1), output_field=IntegerField())),
            partial=Count(Case(When(compliance_status='partial', then=1), output_field=IntegerField())),
            non_compliant=Count(Case(When(compliance_status='non_compliant', then=1), output_field=IntegerField())),
            not_applicable=Count(Case(When(compliance_status='not_applicable', then=1), output_field=IntegerField())),
            in_progress=Count(Case(When(compliance_status='in_progress', then=1), output_field=IntegerField()))
        )
        
        compliance_data['compliance_breakdown'] = status_counts
        
        # Calculate overall compliance percentage
        total = compliance_data['total_links']
        compliant = status_counts['compliant']
        if total > 0:
            compliance_data['overall_compliance_percentage'] = round((compliant / total) * 100, 1)
        
        # Get detailed link information
        compliance_data['links'] = list(links.select_related('standard_section').values(
            'id', 'standard_section__code', 'standard_section__title', 
            'compliance_status', 'notes', 'updated_at'
        ))
        
        return compliance_data
        
    except Document.DoesNotExist:
        return None

def check_standard_compliance(standard_section_id):
    """
    Check compliance status for a specific standard section across all linked documents.
    """
    try:
        standard_section = StandardSection.objects.get(id=standard_section_id)
        links = StandardDocumentLink.objects.filter(standard_section=standard_section)
        
        compliance_data = {
            'standard_section': standard_section,
            'total_documents': links.count(),
            'compliance_breakdown': {},
            'overall_compliance_percentage': 0,
            'links': []
        }
        
        # Count by status
        status_counts = links.aggregate(
            compliant=Count(Case(When(compliance_status='compliant', then=1), output_field=IntegerField())),
            partial=Count(Case(When(compliance_status='partial', then=1), output_field=IntegerField())),
            non_compliant=Count(Case(When(compliance_status='non_compliant', then=1), output_field=IntegerField())),
            not_applicable=Count(Case(When(compliance_status='not_applicable', then=1), output_field=IntegerField())),
            in_progress=Count(Case(When(compliance_status='in_progress', then=1), output_field=IntegerField()))
        )
        
        compliance_data['compliance_breakdown'] = status_counts
        
        # Calculate overall compliance percentage
        total = compliance_data['total_documents']
        compliant = status_counts['compliant']
        if total > 0:
            compliance_data['overall_compliance_percentage'] = round((compliant / total) * 100, 1)
        
        # Get detailed link information
        compliance_data['links'] = list(links.select_related('document').values(
            'id', 'document__title', 'compliance_status', 'notes', 'updated_at'
        ))
        
        return compliance_data
        
    except StandardSection.DoesNotExist:
        return None

def get_overall_compliance_report():
    """
    Generate overall compliance report across all standards and documents.
    """
    all_links = StandardDocumentLink.objects.all()
    
    overall_stats = all_links.aggregate(
        total=Count('id'),
        compliant=Count(Case(When(compliance_status='compliant', then=1), output_field=IntegerField())),
        partial=Count(Case(When(compliance_status='partial', then=1), output_field=IntegerField())),
        non_compliant=Count(Case(When(compliance_status='non_compliant', then=1), output_field=IntegerField())),
        not_applicable=Count(Case(When(compliance_status='not_applicable', then=1), output_field=IntegerField())),
        in_progress=Count(Case(When(compliance_status='in_progress', then=1), output_field=IntegerField()))
    )
    
    total = overall_stats['total']
    compliant = overall_stats['compliant']
    overall_compliance_percentage = round((compliant / total) * 100, 1) if total > 0 else 0
    
    return {
        'overall_stats': overall_stats,
        'overall_compliance_percentage': overall_compliance_percentage,
        'total_standards': StandardSection.objects.count(),
        'total_documents': Document.objects.count(),
        'linked_documents': Document.objects.filter(standard_links__isnull=False).distinct().count(),
        'linked_standards': StandardSection.objects.filter(document_links__isnull=False).distinct().count()
    }
