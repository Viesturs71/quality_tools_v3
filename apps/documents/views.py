from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Document


def document_list(request):
    """View to display list of documents."""
    documents = Document.objects.all()
    return render(request, 'documents/document_list.html', {'documents': documents})


def document_detail(request, pk):
    """View to display document details."""
    document = get_object_or_404(Document, pk=pk)
    return render(request, 'documents/document_detail.html', {'document': document})


@login_required
def document_register(request):
    """View for the document register."""
    return render(request, 'documents/document_register.html', {'page_title': 'Document Register'})


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
