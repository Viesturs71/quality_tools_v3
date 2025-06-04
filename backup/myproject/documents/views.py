from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import DocumentSection, Document

@login_required
def documents_register(request):
    """
    Main Documents Register view showing all document sections
    """
    sections = DocumentSection.objects.filter(parent=None).order_by('name')
    return render(request, 'documents/register/index.html', {
        'sections': sections,
        'title': 'Documents Register'
    })

@login_required
def section_documents(request, section_id):
    """
    View documents within a specific section
    """
    section = get_object_or_404(DocumentSection, id=section_id)
    subsections = DocumentSection.objects.filter(parent=section).order_by('name')
    documents = Document.objects.filter(section=section, status='approved').order_by('-updated_at')
    
    return render(request, 'documents/register/section.html', {
        'section': section,
        'subsections': subsections,
        'documents': documents,
        'title': f'Documents Register - {section.name}'
    })

@login_required
def document_detail(request, document_id):
    """
    View details of a specific document in the register
    """
    document = get_object_or_404(Document, id=document_id, status='approved')
    
    return render(request, 'documents/register/document_detail.html', {
        'document': document,
        'title': f'Document - {document.title}'
    })