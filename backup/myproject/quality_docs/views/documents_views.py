# --- 2. documents_views.py

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView

from quality_docs.forms import QualityDocumentForm
from quality_docs.models.documents import QualityDocument


class DocumentListView(ListView):
    """Class-based view for displaying the list of all documents."""
    model = QualityDocument
    template_name = 'quality_docs/document_list.html'
    context_object_name = 'documents'
    paginate_by = 10

@login_required
def document_create(request):
    """
    Create a new document.
    Any logged-in user can create and submit documents.
    """
    if request.method == "POST":
        form = QualityDocumentForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            document = form.save(commit=False)
            document.created_by = request.user
            document.status = "draft"
            document.save()

            # Log the document creation
            try:
                from quality_docs.models.logs import DocumentLog
                DocumentLog.objects.create(
                    document=document,
                    user=request.user,
                    action="create"
                )
            except ImportError:
                # If DocumentLog doesn't exist, just continue
                pass

            messages.success(
                request,
                _(f"✅ Document '{document.title}' has been successfully created.")
            )

            # Redirect to document detail page
            return redirect("quality_docs:document_detail", doc_id=document.id)
    else:
        # Initialize form with user context
        form = QualityDocumentForm(user=request.user)

    return render(request, "quality_docs/document_form.html", {
        "form": form,
        "title": _("Create New Document"),
        "submit_text": _("Create Document")
    })

@login_required
def document_list(request):
    """
    Display a tree structure of documents organized by sections.
    """

    from quality_docs.models.sections import DocumentSection

    # Get all approved documents
    approved_documents = QualityDocument.objects.filter(
        status="approved"
    ).select_related('document_type', 'created_by')

    # Get all document sections ordered by identifier
    sections = DocumentSection.objects.all().order_by('identifier')

    # Create a dictionary to store documents by section
    documents_by_section = {}
    for section in sections:
        # Find documents that belong to this section
        section_documents = approved_documents.filter(
            section=section
        ).distinct()

        if section_documents.exists():
            documents_by_section[section] = section_documents

    # Get documents without sections
    documents_without_section = approved_documents.filter(
        section__isnull=True
    ).distinct()

    context = {
        'documents_by_section': documents_by_section,
        'documents_without_section': documents_without_section,
        'sections': sections,
    }

    return render(request, 'quality_docs/document_list.html', context)

@login_required
def document_detail(request, doc_id):
    """
    Displays the detailed view of the document.
    Shows appropriate actions based on document status and user permissions.
    """
    document = get_object_or_404(QualityDocument, id=doc_id)

    # Get user's approval record if exists
    user_approval = None
    if request.user.is_authenticated:
        user_approval = ApprovalFlow.objects.filter(
            document=document,
            approver=request.user
        ).first()

    context = {
        'document': document,
        'user_approval': user_approval,
        'can_edit': document.status == 'draft' and (
            request.user == document.created_by or request.user.is_staff
        ),
        'can_submit': document.status == 'draft' and (
            request.user == document.created_by or request.user.is_staff
        ),
        'can_approve': user_approval and user_approval.status == 'pending' and user_approval.is_active_for_approval()
    }

    return render(request, "quality_docs/document_detail.html", context)

@login_required
def document_edit(request, doc_id):
    document = get_object_or_404(QualityDocument, id=doc_id)
    if request.method == "POST":
        form = QualityDocumentForm(request.POST, request.FILES, instance=document, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("quality_docs:document_detail", doc_id=document.id)
    else:
        form = QualityDocumentForm(instance=document, user=request.user)
    return render(request, "quality_docs/document_form.html", {"form": form, "document": document})

@login_required
def document_delete(request, doc_id):
    document = get_object_or_404(QualityDocument, id=doc_id)
    if request.method == "POST":
        document.delete()
        messages.success(request, "✅ The document was successfully deleted.")
        return redirect("quality_docs:document_list")
    return render(request, "quality_docs/document_confirm_delete.html", {"document": document})

@login_required
def preview_pdf(request, doc_id):
    document = get_object_or_404(QualityDocument, id=doc_id)
    if not document.file:
        messages.error(request, "❌ The document does not have a PDF file attached.")
        return redirect("quality_docs:document_detail", doc_id=doc_id)
    return render(request, "quality_docs/document_preview.html", {"document": document})

@login_required
def download_pdf(request, doc_id):
    document = get_object_or_404(QualityDocument, id=doc_id)
    if not document.file:
        messages.error(request, "❌ The document does not have a PDF file attached.")
        return redirect("quality_docs:document_detail", doc_id=doc_id)
    try:
        response = FileResponse(open(document.file.path, "rb"), content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{document.file.name}"'
        return response
    except FileNotFoundError:
        raise Http404("PDF file not found.")

@login_required
def publish_document(request, doc_id):
    document = get_object_or_404(QualityDocument, id=doc_id)
    document.status = "published"
    document.save()
    return redirect("quality_docs:document_detail", doc_id=document.id)

@login_required
def document_overview(request):
    """
    View for document overview
    """
    from django.shortcuts import render
    return render(request, 'quality_docs/document_overview.html', {'title': 'Document Overview'})

@login_required
def document_update(request, doc_id):  # Mainīts no pk uz doc_id
    document = get_object_or_404(QualityDocument, id=doc_id)
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            return redirect('quality_docs:document_detail', pk=document.pk)
    else:
        form = DocumentForm(instance=document)

    return render(request, 'quality_docs/document_form.html', {'form': form})

@login_required
@permission_required('quality_docs.can_approve_documents', raise_exception=True)
def documents_for_approval(request):
    """
    View to list documents that are awaiting approval.
    """
    documents = QualityDocument.objects.filter(status='awaiting_approval')
    return render(request, 'quality_docs/documents_for_approval.html', {'documents': documents})

@login_required
def submit_document_for_approval(request, doc_id):
    """
    Allow any user to submit their document for approval.
    Changes document status from draft to submitted.
    """
    document = get_object_or_404(QualityDocument, id=doc_id)

    # Security check - only document creator or staff can submit
    if document.created_by != request.user and not request.user.is_staff:
        messages.error(request, _("You don't have permission to submit this document."))
        return redirect("quality_docs:document_detail", doc_id=document.id)

    # Only draft documents can be submitted
    if document.status != "draft":
        messages.error(request, _("Only draft documents can be submitted for approval."))
        return redirect("quality_docs:document_detail", doc_id=document.id)

    if request.method == "POST":
        # Mainām statusu uz "submitted" nevis "pending_approval"
        document.status = "submitted"
        document.save()

        # Sūtam paziņojumu kvalitātes vadītājiem
        try:
            send_notification_to_quality_managers(document)
        except Exception:
            # Log the error but continue
            pass

        messages.success(request, _("Document has been submitted and is waiting for quality manager review."))
        return redirect("quality_docs:document_detail", doc_id=document.id)

    return render(request, "quality_docs/submit_document.html", {"document": document})

def send_notification_to_quality_managers(document):
    """
    Send notification to all users with quality_manager permission
    """
    from django.conf import settings
    from django.contrib.auth import get_user_model
    from django.core.mail import send_mail
    from django.db.models import Q

    User = get_user_model()

    # Atrodam kvalitātes vadītājus (lietotājus ar noteiktām atļaujām)
    quality_managers = User.objects.filter(
        Q(groups__permissions__codename='can_manage_approval_flow') |
        Q(user_permissions__codename='can_manage_approval_flow')
    ).distinct()

    # Ja ir iespējots e-pasta sūtīšana, sūtam paziņojumus
    if hasattr(settings, 'EMAIL_BACKEND') and settings.EMAIL_BACKEND:
        subject = f"New document submitted: {document.title}"
        message = f"""
        A new document has been submitted for approval:

        Title: {document.title}
        Type: {document.document_type}
        ID: {document.document_identifier}
        Submitted by: {document.created_by.get_full_name() or document.created_by.username}

        Please review this document and set up the approval workflow.
        """

        for manager in quality_managers:
            if manager.email:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [manager.email],
                    fail_silently=True,
                )

@login_required
def my_documents(request):
    """
    Display documents created by the current user.
    This view shows all documents that the user has created or is involved with.
    """
    # Get all documents created by the current user
    created_documents = QualityDocument.objects.filter(created_by=request.user).order_by('-created_at')

    # Get all documents where the user is a reviewer
    reviewing_documents = QualityDocument.objects.filter(
        approval_flows__approver=request.user
    ).exclude(created_by=request.user).distinct().order_by('-created_at')

    # Add user-specific approval information to each document
    for doc in reviewing_documents:
        doc.user_approval = doc.approval_flows.filter(approver=request.user).first()

    context = {
        'created_documents': created_documents,
        'reviewing_documents': reviewing_documents,
    }

    return render(request, 'quality_docs/my_documents.html', context)
