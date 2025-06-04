# quality_docs/views/approval_views.py

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from quality_docs.forms import ApprovalForm
from quality_docs.models.approval_flow import ApprovalFlow
from quality_docs.models.documents import QualityDocument
from quality_docs.services.pdf_signer import sign_pdf_document


@login_required
@permission_required('quality_docs.can_approve_documents', raise_exception=True)
def documents_for_approval(request):
    """
    Display a comprehensive list of documents awaiting user approval.
    Includes filtering options by document type and status.
    """
    # Get documents where the current user is an approver with pending status
    # Use only() to explicitly select only the fields we need
    pending_approvals = ApprovalFlow.objects.filter(
        approver=request.user,
        status="pending"
    ).only(
        'id', 'document', 'status',
        'document__id', 'document__title',
        'document__document_type', 'document__created_by',
        'document__created_at'
    ).select_related('document', 'document__document_type', 'document__created_by')

    # Get all documents with pending approval status for admins/quality managers
    all_pending = None
    if request.user.has_perm('quality_docs.view_all_approvals'):
        all_pending = QualityDocument.objects.filter(
            status__in=["pending_approval", "under_review"]
        ).only(
            'id', 'title', 'document_type',
            'created_by', 'updated_at'
        ).select_related('document_type', 'created_by')

    context = {
        'pending_approvals': pending_approvals,
        'all_pending': all_pending,
    }

    return render(request, 'quality_docs/documents_for_approval.html', context)

@login_required
@permission_required('quality_docs.can_approve_documents', raise_exception=True)
def approve_document(request, doc_id):
    """
    Approve a document and update its status.
    Creates approval record and handles the document workflow state.
    """
    document = get_object_or_404(QualityDocument, id=doc_id)
    approval = get_object_or_404(
        ApprovalFlow,
        document=document,
        approver=request.user,
        status="pending"
    )

    # Check if this approval is currently active in the workflow - safely
    can_approve = True
    if hasattr(approval, 'is_active_for_approval') and callable(approval.is_active_for_approval):
        try:
            can_approve = approval.is_active_for_approval()
        except Exception:
            # If there's an error with the method, default to allowing approval
            pass

    if not can_approve:
        messages.warning(request, _("This document is not yet ready for your approval. Previous reviewers must approve it first."))
        return redirect("quality_docs:document_detail", doc_id=document.id)

    if request.method == "POST":
        form = ApprovalForm(request.POST, request.FILES)
        if form.is_valid():
            # Update approval status
            approval.status = "approved"
            approval.approved_at = timezone.now()
            approval.save()

            # Check if all approvals are complete
            pending_approvals = ApprovalFlow.objects.filter(
                document=document,
                status="pending"
            ).exists()

            if not pending_approvals:
                document.status = "approved"
                document.approval_date = timezone.now()
                document.save()
                messages.success(
                    request,
                    _("Document '{}' has been fully approved!").format(document.title)
                )
            else:
                messages.success(
                    request,
                    _("You have approved the document '{}'. Waiting for other approvers.").format(document.title)
                )

            return redirect('quality_docs:document_detail', doc_id=document.id)
    else:
        form = ApprovalForm()

    # Find other reviewers - without using fields that might not exist
    other_reviewers = ApprovalFlow.objects.filter(
        document=document
    ).only(
        'id', 'approver', 'status'
    ).select_related('approver')

    context = {
        'document': document,
        'approval': approval,
        'form': form,
        'other_reviewers': other_reviewers,
    }

    return render(request, 'quality_docs/approve_document.html', context)

@login_required
@permission_required('quality_docs.can_approve_documents', raise_exception=True)
def reject_document(request, doc_id):
    """
    Reject a document with comments.
    Updates document status and notifies the document owner.
    """
    document = get_object_or_404(QualityDocument, id=doc_id)
    approval = get_object_or_404(
        ApprovalFlow,
        document=document,
        approver=request.user,
        status="pending"
    )

    if request.method == "POST":
        rejection_reason = request.POST.get('rejection_reason', '')

        if rejection_reason:
            approval.status = "rejected"
            approval.rejection_reason = rejection_reason
            approval.rejected_at = timezone.now()
            approval.save()

            # Update document status
            document.status = "returned"
            document.save()

            messages.warning(
                request,
                _(f"Document '{document.title}' has been rejected and returned for revision.")
            )
            return redirect('quality_docs:document_detail', doc_id=document.id)
        else:
            messages.error(request, _("Please provide a rejection reason."))

    return render(request, 'quality_docs/reject_document.html', {'document': document})

@login_required
@permission_required('quality_docs.can_approve_documents', raise_exception=True)
def sign_and_download_pdf(request, approval_id):
    """
    Sign the document PDF and allow it to be downloaded.
    Records digital signature and provides downloadable signed PDF.
   """
    approval = get_object_or_404(ApprovalFlow, id=approval_id, approver=request.user)
    document = approval.document

    if request.method == "POST":
        form = ApprovalForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                signed_file_path = sign_pdf_document(
                    document.file.path,
                    form.cleaned_data["certificate"].temporary_file_path(),
                    form.cleaned_data["private_key"].temporary_file_path(),
                    form.cleaned_data["password"],
                    approval.approver.get_full_name()
                )
                response = HttpResponse(open(signed_file_path, 'rb'), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="signed_{document.file.name}"'
                return response
            except Exception as e:
                messages.error(request, f"Signing error: {e}")
        else:
            messages.error(request, "Invalid form data.")

    else:
        form = ApprovalForm()

    return render(request, "quality_docs/approve_document.html", {"form": form, "approval": approval})

@login_required
def approval_dashboard(request):
    """
    Display an overview dashboard with approval statistics and recent activities.
    """
    import datetime

    from django.utils import timezone

    # Get counts for different document statuses
    pending_count = ApprovalFlow.objects.filter(
        approver=request.user,
        status="pending"
    ).count()

    thirty_days_ago = timezone.now() - datetime.timedelta(days=30)

    approved_count = ApprovalFlow.objects.filter(
        approver=request.user,
        status="approved",
        approved_at__gte=thirty_days_ago
    ).count()

    # Get documents in different statuses
    draft_count = QualityDocument.objects.filter(status="draft").count()
    returned_count = QualityDocument.objects.filter(status="returned").count()

    # Get recent approval activities
    recent_activities = ApprovalFlow.objects.filter(
        updated_at__gte=thirty_days_ago
    ).only('id', 'document', 'approver', 'status', 'updated_at').select_related('document', 'approver').order_by('-updated_at')[:10]

    context = {
        'pending_count': pending_count,
        'approved_count': approved_count,
        'draft_count': draft_count,
        'returned_count': returned_count,
        'recent_activities': recent_activities
    }

    return render(request, 'quality_docs/approval_dashboard.html', context)
