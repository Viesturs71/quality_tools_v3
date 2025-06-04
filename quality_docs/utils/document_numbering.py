import datetime
from django.utils.translation import gettext_lazy as _
from django.db.models import Max
from django.core.exceptions import ValidationError

def generate_document_number(company, document_type, section=None, year=None):
    """
    Ģenerē dokumenta numuru formātā: [COMPANY]-[DOCTYPE]-[SECTION]-[YEAR]-[SEQUENTIAL]
    
    Piemērs: ABC-QM-01-2023-001
    
    :param company: Uzņēmums, kam pieder dokuments
    :param document_type: Dokumenta tips
    :param section: Dokumenta sadaļa (opcionāli)
    :param year: Gads (opcionāli, noklusējums - pašreizējais gads)
    :return: Ģenerēts dokumenta numurs
    """
    if not company or not company.identifier:
        raise ValidationError(_("Company with valid identifier is required"))
    
    if not document_type or not document_type.abbreviation:
        raise ValidationError(_("Document type with valid abbreviation is required"))
    
    # Ja gads nav norādīts, izmantot pašreizējo gadu
    if not year:
        year = datetime.date.today().year
    
    # Sadaļas identifikators (ja nav norādīts, izmantot '00')
    section_id = section.identifier if section and hasattr(section, 'identifier') else '00'
    
    # Pamatne dokumenta numuram bez secības numura
    base_number = f"{company.identifier}-{document_type.abbreviation}-{section_id}-{year}"
    
    # Atrast lielāko secības numuru ar šo pamatni
    from ..models import QualityDocument
    
    # Filtrēt pēc numura, kas sākas ar šo pamatni
    max_seq = QualityDocument.objects.filter(
        document_number__startswith=base_number
    ).aggregate(
        max_seq=Max('document_number')
    )['max_seq']
    
    # Ja nav ierakstu, sākt ar 001
    if not max_seq:
        next_seq = 1
    else:
        # Iegūt pēdējo secības numuru un palielināt par 1
        try:
            last_seq = int(max_seq.split('-')[-1])
            next_seq = last_seq + 1
        except (ValueError, IndexError):
            next_seq = 1
    
    # Formatēt secības numuru ar vadošajām nullēm (001, 002, utt.)
    return f"{base_number}-{next_seq:03d}"

def validate_document_number_format(document_number):
    """
    Pārbauda, vai dokumenta numurs atbilst formātam.
    
    Formāts: [COMPANY]-[DOCTYPE]-[SECTION]-[YEAR]-[SEQUENTIAL]
    Piemērs: ABC-QM-01-2023-001
    
    :param document_number: Dokumenta numurs pārbaudei
    :return: True, ja formāts ir pareizs, citādi ValidationError
    """
    import re
    
    # Regulārā izteiksme formāta pārbaudei
    pattern = r'^[A-Z0-9]{2,4}-[A-Z0-9]{1,5}-[A-Z0-9]{1,3}-\d{4}-\d{3,}$'
    
    if not re.match(pattern, document_number):
        raise ValidationError(
            _("Invalid document number format. Format should be: COMPANY-DOCTYPE-SECTION-YEAR-NUMBER")
        )
    
    return True

def validate_document_number_uniqueness(document_number, document_id=None):
    """
    Pārbauda, vai dokumenta numurs ir unikāls sistēmā.
    
    :param document_number: Dokumenta numurs pārbaudei
    :param document_id: Pašreizējā dokumenta ID (ja rediģējam), lai izslēgtu no pārbaudes
    :return: True, ja numurs ir unikāls, citādi ValidationError
    """
    from ..models import QualityDocument
    
    # Izveidot vaicājumu, lai pārbaudītu, vai numurs jau eksistē
    query = QualityDocument.objects.filter(document_number=document_number)
    
    # Ja rediģējam esošu dokumentu, izslēgt to no pārbaudes
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
    Sadalīt dokumenta numuru sastāvdaļās analīzei.
    
    :param document_number: Dokumenta numurs
    :return: Vārdnīca ar numura sastāvdaļām (company, doctype, section, year, sequence)
    """
    try:
        parts = document_number.split('-')
        if len(parts) != 5:
            return None
        
        return {
            'company': parts[0],
            'doctype': parts[1],
            'section': parts[2],
            'year': parts[3],
            'sequence': parts[4]
        }
    except (ValueError, IndexError, AttributeError):
        return None

def suggest_next_sequence_number(document_number_base):
    """
    Iesaka nākamo secības numuru, pamatojoties uz esošo dokumentu numuru pamatni.
    
    :param document_number_base: Dokumenta numura pamatne (bez secības numura)
    :return: Nākamais ieteicamais secības numurs
    """
    from ..models import QualityDocument
    
    # Atrast lielāko secības numuru ar šo pamatni
    max_seq = QualityDocument.objects.filter(
        document_number__startswith=document_number_base
    ).aggregate(
        max_seq=Max('document_number')
    )['max_seq']
    
    # Ja nav ierakstu, sākt ar 001
    if not max_seq:
        next_seq = 1
    else:
        # Iegūt pēdējo secības numuru un palielināt par 1
        try:
            last_seq = int(max_seq.split('-')[-1])
            next_seq = last_seq + 1
        except (ValueError, IndexError):
            next_seq = 1
    
    return next_seq
