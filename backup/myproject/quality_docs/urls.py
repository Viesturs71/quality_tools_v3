# quality_docs/urls.py

from django.urls import path

from quality_docs.views.approval_views import (
    approval_dashboard,
    approve_document,
    documents_for_approval,
    reject_document,
    sign_and_download_pdf,
)
from quality_docs.views.documents.step1 import Step1View
from quality_docs.views.documents_views import (
    document_create,
    document_delete,
    document_detail,
    document_list,
    document_update,
    my_documents,
    submit_document_for_approval,  # Pārvietots šeit no approval_views
)
from quality_docs.views.quality_manager_views import (
    return_document,
    setup_approval_flow,
    submitted_documents_list,
)
from quality_docs.views.reconciliation_views import (
    DocumentReconciliationListView,
)
from quality_docs.views.standards_views import (
    StandardListView,
)

app_name = "quality_docs"

urlpatterns = [
    # Dokumenti - mainām URL parametrus, lai tie atbilstu skatu funkcijām
    path('documents/', document_list, name='document_list'),
    path('documents/create/', document_create, name='document_create'),
    path('documents/<int:doc_id>/', document_detail, name='document_detail'),
    path('documents/<int:doc_id>/edit/', document_update, name='document_update'),  # Mainīts no pk uz doc_id
    path('documents/<int:doc_id>/delete/', document_delete, name='document_delete'),
path('documents/my/', my_documents, name='my_documents'),
    path('documents/<int:doc_id>/submit/', submit_document_for_approval, name='submit_document_for_approval'),

    # Quality Manager Views
    path('documents/submitted/', submitted_documents_list, name='submitted_documents_list'),
    path('documents/<int:doc_id>/setup-approval/', setup_approval_flow, name='setup_approval_flow'),
    path('documents/<int:doc_id>/return/', return_document, name='return_document'),

    # Approval workflows
    path('documents/for-approval/', documents_for_approval, name='documents_for_approval'),
    path('documents/<int:doc_id>/approve/', approve_document, name='approve_document'),
path('documents/<int:doc_id>/reject/', reject_document, name='reject_document'),
    path('sign/<int:approval_id>/', sign_and_download_pdf, name='sign_and_download_pdf'),
     path('approval/dashboard/', approval_dashboard, name='approval_dashboard'),

    # Document creation workflow
    path('documents/<int:doc_id>/step1/', Step1View.as_view(), name='document_step1'),

# Standards
    path('standards/', StandardListView.as_view(), name='standard_list'),

# Reconciliation
    path('documents/reconciliation/', DocumentReconciliationListView.as_view(), name='documents_for_reconciliation'),
    ]
