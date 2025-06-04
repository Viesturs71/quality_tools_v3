# quality_docs/views/reconciliation.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from quality_docs.models.approval_flow import ApprovalFlow


class DocumentReconciliationListView(LoginRequiredMixin, ListView):
    """View to list documents that require reconciliation (approval)."""
    model = ApprovalFlow
    template_name = "quality_docs/document_reconciliation_list.html"
    context_object_name = "approvals"
    paginate_by = 10

    def get_queryset(self):
        """Filter approvals that are still pending."""
        return ApprovalFlow.objects.filter(status="pending").select_related('document', 'approver')
