# apps/standards/models/__init__.py

from .standard               import Standard
from .standard_category      import StandardCategory
from .standard_section       import StandardSection
from .standard_requirement   import StandardRequirement
from .standard_attachment    import StandardAttachment
from .standard_document      import StandardDocument
from .standard_document_link import StandardDocumentLink
from .standard_compliance    import StandardCompliance
from .standard_revision      import StandardRevision

# if any code elsewhere expects this legacy name:
StandardSectionDocumentLink = StandardDocumentLink

__all__ = [
    'Standard', 'StandardCategory',
    'StandardSection', 'StandardRequirement',
    'StandardAttachment', 'StandardDocument',
    'StandardDocumentLink', 'StandardCompliance',
    'StandardRevision', 'StandardSectionDocumentLink'
]
