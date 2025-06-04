# quality_docs/urls.py

from django.urls import path
from quality_docs.views import (
    home,
    document_list,
    document_detail,
    document_create,
    document_update,
    document_delete,
    document_sign,
    document_download,
    approval_flow_create,
    approval_step_create,
    document_review_create,
    signature_request_create,
    document_distribution_create,
)

app_name = 'quality_docs'

urlpatterns = [
    path('', home, name='home'),
    path('documents/', document_list, name='document_list'),
    path('documents/<int:pk>/', document_detail, name='document_detail'),
    path('documents/create/', document_create, name='document_create'),
    path('documents/<int:pk>/update/', document_update, name='document_update'),
    path('documents/<int:pk>/delete/', document_delete, name='document_delete'),
    path('documents/<int:pk>/approve/', document_update, name='document_approve'),
    path('documents/<int:pk>/sign/', document_sign, name='document_sign'),
    path('documents/<int:pk>/download/', document_download, name='document_download'),
    path('approval-flow/<int:document_id>/create/', approval_flow_create, name='approval_flow_create'),
    path('approval-step/<int:flow_id>/create/', approval_step_create, name='approval_step_create'),
    path('review/<int:document_id>/create/', document_review_create, name='document_review_create'),
    path('signature-request/<int:step_id>/create/', signature_request_create, name='signature_request_create'),
    path('distribution/<int:document_id>/create/', document_distribution_create, name='document_distribution_create'),
]
