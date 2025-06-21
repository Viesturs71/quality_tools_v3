from django.urls import path
from .views.document_views import (
    DocumentListView, DocumentDetailView,
    DocumentCreateView, DocumentUpdateView, DocumentDeleteView,
    user_documents, register_document
)

app_name = 'documents'

urlpatterns = [
    path('', DocumentListView.as_view(), name='document_list'),
    path('register/', register_document, name='document_register'),
    path('user-documents/', user_documents, name='user_documents'),
    path('<int:pk>/', DocumentDetailView.as_view(), name='document_detail'),
    path('<int:pk>/edit/', DocumentUpdateView.as_view(), name='document_update'),
    path('<int:pk>/delete/', DocumentDeleteView.as_view(), name='document_delete'),
]
