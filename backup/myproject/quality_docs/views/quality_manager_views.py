from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from quality_docs.forms.workflow_setup import ApprovalFlowSetupForm
from quality_docs.models.approval_flow import ApprovalFlow
from quality_docs.models.documents import DocumentType, QualityDocument

User = get_user_model()

@login_required
@permission_required('quality_docs.can_manage_approval_flow', raise_exception=True)
def submitted_documents_list(request):
    """
    View for quality managers to see all submitted documents waiting for workflow setup.
    """
    submitted_documents = QualityDocument.objects.filter(status="submitted")

    # Get document types and users for filters
    document_types = DocumentType.objects.all()
    users = User.objects.filter(is_active=True)

    # Filtrēšanas opcijas
    document_type = request.GET.get('document_type')
    created_by = request.GET.get('created_by')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    if document_type:
        submitted_documents = submitted_documents.filter(document_type__id=document_type)

    if created_by:
        submitted_documents = submitted_documents.filter(created_by__id=created_by)

    if date_from:
        submitted_documents = submitted_documents.filter(created_at__gte=date_from)

    if date_to:
        submitted_documents = submitted_documents.filter(created_at__lte=date_to)

    context = {
        'submitted_documents': submitted_documents,
        'document_types': document_types,
        'users': users,
        'filter_params': {
            'document_type': document_type,
            'created_by': created_by,
            'date_from': date_from,
            'date_to': date_to
        }
    }

    return render(request, 'quality_docs/submitted_documents.html', context)

@login_required
@permission_required('quality_docs.can_manage_approval_flow', raise_exception=True)
def setup_approval_flow(request, doc_id):
    """
    Allow quality manager to set up the document approval workflow.
    """
    document = get_object_or_404(QualityDocument, id=doc_id)

    # Checking if document is in correct state
    if document.status != "submitted":
        messages.error(request, _("This document is not available for workflow setup."))
        return redirect("quality_docs:submitted_documents_list")

    if request.method == "POST":
        form = ApprovalFlowSetupForm(request.POST, document=document)
        if form.is_valid():
            # Mainām dokumenta statusu
            document.status = "under_review"
            document.save()

            # Saglabājam plūsmu
            reviewers = form.cleaned_data.get('reviewers')
            review_type = form.cleaned_data.get('review_type')
            document.review_type = review_type
            document.save()

            # Dzēšam vecās plūsmas (ja tādas ir)
            ApprovalFlow.objects.filter(document=document).delete()

            # Izveidojam jaunās plūsmas atkarībā no izvēlētā režīma
            if review_type == 'sequential':
                # Secīga apstiprināšana - katrs apstiprinātājs ir savā grupā ar unikālu secības numuru
                for i, reviewer in enumerate(reviewers, 1):
                    ApprovalFlow.objects.create(
                        document=document,
                        approver=reviewer,
                        status="pending",
                        approval_group=i,
                        review_order=i
                    )
            elif review_type == 'parallel':
                # Paralēla apstiprināšana - visi apstiprinātāji ir vienā grupā
                for reviewer in reviewers:
                    ApprovalFlow.objects.create(
                        document=document,
                        approver=reviewer,
                        status="pending",
                        approval_group=1,
                        review_order=1
                    )
            else:  # combined
                # Kombinētā apstiprināšana - apstiprinātāji ir sadalīti pa grupām
                approval_groups = form.cleaned_data.get('approval_groups', {})

                if approval_groups:
                    try:
                        groups_data = json.loads(approval_groups)
                        for group_order, group_data in groups_data.items():
                            group_order = int(group_order)
                            group_reviewers = group_data.get('reviewers', [])

                            for reviewer_id in group_reviewers:
                                ApprovalFlow.objects.create(
                                    document=document,
                                    approver_id=reviewer_id,
                                    status="pending",
                                    approval_group=group_data.get('group_id', group_order),
                                    review_order=group_order
                                )
                    except (json.JSONDecodeError, ValueError, KeyError):
                        # Ja radās kļūda, izmantojam vienkāršu secīgo režīmu
                        for i, reviewer in enumerate(reviewers, 1):
                            ApprovalFlow.objects.create(
                                document=document,
                                approver=reviewer,
                                status="pending",
                                approval_group=i,
                                review_order=i
                            )
                else:
                    # Ja nav norādītas grupas, izmantojam vienkāršu secīgo režīmu
                    for i, reviewer in enumerate(reviewers, 1):
                        ApprovalFlow.objects.create(
                            document=document,
                            approver=reviewer,
                            status="pending",
                            approval_group=i,
                            review_order=i
                        )

            messages.success(request, _("Approval workflow has been set up successfully."))
            return redirect("quality_docs:document_detail", doc_id=document.id)
    else:
        # Preload existing reviewers if any
        initial = {}
        existing_reviewers = document.reviewers.all()
        if existing_reviewers:
            initial['reviewers'] = existing_reviewers
            initial['review_type'] = document.review_type

        form = ApprovalFlowSetupForm(document=document, initial=initial)

    return render(request, 'quality_docs/setup_approval_flow.html', {
        'form': form,
        'document': document
    })

@login_required
@permission_required('quality_docs.can_manage_approval_flow', raise_exception=True)
@require_POST
def return_document(request, doc_id):
    """
    Return the document to creator for fixes before setting up approval flow.
    """
    document = get_object_or_404(QualityDocument, id=doc_id)

    if document.status != "submitted":
        messages.error(request, _("Only submitted documents can be returned."))
        return redirect("quality_docs:submitted_documents_list")

    return_reason = request.POST.get('return_reason', '')

    if not return_reason:
        messages.error(request, _("Please provide a reason for returning the document."))
        return redirect("quality_docs:setup_approval_flow", doc_id=document.id)

    document.status = "returned"
    document.review_comment = return_reason
    document.save()

    messages.success(request, _("The document has been returned to the creator for revision."))
    return redirect("quality_docs:submitted_documents_list")
