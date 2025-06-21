from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.documents.models.document import Document  # Corrected import path
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.documents.forms import DocumentForm  # Corrected import path

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


@login_required
def register_document(request):
    """View for registering a new document."""
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.uploaded_by = request.user
            doc.created_by = request.user  # Set the created_by field to the logged-in user
            doc.save()
            return redirect('documents:user_documents')
    else:
        form = DocumentForm()
    return render(request, 'documents/document_register.html', {
        'form': form,
    })

@login_required
def user_documents(request):
    """View for displaying documents uploaded by the user."""
    docs = Document.objects.filter(uploaded_by=request.user)  # Ensure this matches the model field
    return render(request, 'documents/user_documents.html', {'documents': docs})