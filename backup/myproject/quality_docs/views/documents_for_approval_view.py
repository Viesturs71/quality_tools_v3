#quality_docs/views/documents_for_approval_view.py
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render

from quality_docs.models.documents import QualityDocument


@login_required
@permission_required('quality_docs.can_approve_documents', raise_exception=True)
def documents_for_approval(request):
    """
    View to list documents that are awaiting approval.
    """
    documents = QualityDocument.objects.filter(status='awaiting_approval')
    return render(request, 'quality_docs/documents_for_approval.html', {'documents': documents})
