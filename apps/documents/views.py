"""
Re-export views from the views package for backward compatibility.
"""
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Document
from .views.document_views import (
    register_document, user_documents
)

# Function-based views for backward compatibility
def document_list(request):
    """Redirects to class-based view."""
    return DocumentListView.as_view()(request)

def document_detail(request, pk):
    """Redirects to class-based view."""
    return DocumentDetailView.as_view()(request, pk=pk)

def document_register(request):
    """Redirects to register_document function."""
    return register_document(request)
__all__ = [
    'DocumentListView', 'DocumentDetailView', 'DocumentCreateView',
    'DocumentUpdateView', 'DocumentDeleteView', 'document_list',
    'document_detail', 'document_register', 'register_document',
    'user_documents'
]


class DocumentListView(ListView):
    model = Document
    template_name = 'documents/document_list.html'
    context_object_name = 'documents'


class DocumentDetailView(DetailView):
    model = Document
    template_name = 'documents/document_detail.html'
    context_object_name = 'document'


class DocumentCreateView(CreateView):
    model = Document
    fields = ['title', 'content', 'uploaded_by']
    template_name = 'documents/document_form.html'
    success_url = reverse_lazy('documents:document_list')


class DocumentUpdateView(UpdateView):
    model = Document
    fields = ['title', 'content']
    template_name = 'documents/document_form.html'
    success_url = reverse_lazy('documents:document_list')


class DocumentDeleteView(DeleteView):
    model = Document
    template_name = 'documents/document_confirm_delete.html'
    success_url = reverse_lazy('documents:document_list')
