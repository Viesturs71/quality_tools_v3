import datetime
from django.utils.translation import gettext_lazy as _
from django.db.models import Max
from django.core.exceptions import ValidationError


def get_document_model():
    """
    Lazily import the Document model to avoid circular imports.
    """
    from apps.documents.models import Document
    return Document


def generate_document_number(company=None, document_type=None, section=None, year=None):
    """
    Generate a document number. If no parameters provided, generates a simple DOC-XXX format.
    Otherwise generates: [COMPANY]-[DOCTYPE]-[SECTION]-[YEAR]-[SEQUENTIAL]
    Example: ABC-QM-01-2023-001 or DOC-001
    """
    if not company:
        # Simple format for basic documents
        Document = get_document_model()
        max_doc = Document.objects.filter(
            document_number__startswith='DOC-'
        ).aggregate(max_seq=Max('document_number'))['max_seq']
        
        next_seq = 1
        if max_doc:
            try:
                current_seq = int(max_doc.split('-')[-1])
                next_seq = current_seq + 1
            except (ValueError, IndexError):
                next_seq = 1
        
        return f"DOC-{next_seq:03d}"
    
    # Complex format with parameters
    if not company.identifier:
        raise ValidationError(_("Company with valid identifier is required"))

    if not document_type or not document_type.abbreviation:
        raise ValidationError(_("Document type with valid abbreviation is required"))

    year = year or datetime.date.today().year
    section_id = section.identifier if section and hasattr(section, 'identifier') else '00'
    base_number = f"{company.identifier}-{document_type.abbreviation}-{section_id}-{year}"

    Document = get_document_model()
    max_seq = Document.objects.filter(
        document_number__startswith=base_number
    ).aggregate(max_seq=Max('document_number'))['max_seq']

    next_seq = 1 if not max_seq else int(max_seq.split('-')[-1]) + 1
    return f"{base_number}-{next_seq:03d}"


def validate_document_number_format(document_number):
    """
    Validate the format of a document number.
    Format: [COMPANY]-[DOCTYPE]-[SECTION]-[YEAR]-[SEQUENTIAL]
    """
    import re
    pattern = r'^[A-Z0-9]{2,4}-[A-Z0-9]{1,5}-[A-Z0-9]{1,3}-\d{4}-\d{3,}$'
    if not re.match(pattern, document_number):
        raise ValidationError(
            _("Invalid document number format. Format should be: COMPANY-DOCTYPE-SECTION-YEAR-NUMBER")
        )
    return True


def validate_document_number_uniqueness(document_number, document_id=None):
    """
    Validate the uniqueness of a document number in the system.
    """
    Document = get_document_model()
    query = Document.objects.filter(document_number=document_number)
    if document_id is not None:
        query = query.exclude(id=document_id)

    if query.exists():
        raise ValidationError(
            _("Document number '%(number)s' already exists in the system. Please use a different number."),
            params={'number': document_number}
        )
    return True


def parse_document_number(document_number):
    """
    Parse a document number into its components.
    """
    try:
        parts = document_number.split('-')
        if len(parts) == 2:  # Simple format DOC-001
            return {
                'type': parts[0],
                'sequence': parts[1]
            }
        elif len(parts) == 5:  # Complex format
            return {
                'company': parts[0],
                'doctype': parts[1],
                'section': parts[2],
                'year': parts[3],
                'sequence': parts[4]
            }
        return None
    except (ValueError, IndexError, AttributeError):
        return None


def suggest_next_sequence_number(document_number_base):
    """
    Suggest the next sequence number based on the existing document number base.
    """
    Document = get_document_model()
    max_seq = Document.objects.filter(
        document_number__startswith=document_number_base
    ).aggregate(max_seq=Max('document_number'))['max_seq']

    next_seq = 1 if not max_seq else int(max_seq.split('-')[-1]) + 1
    return next_seq
