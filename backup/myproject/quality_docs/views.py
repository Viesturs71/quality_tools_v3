# quality_docs/views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.http import FileResponse, Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.encoding import smart_str
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from rest_framework import viewsets

from quality_docs.forms import BasicQualityDocumentForm
from quality_docs.models import QualityDocument
from quality_docs.models.sections import DocumentSection
from quality_docs.services.pdf_signer import sign_pdf_document

from .forms import ApprovalForm, QualityDocumentForm
from .models.approval_flow import ApprovalFlow
from .models.documents import QualityDocument
from .models.logs import DocumentLog
from .models.standards import Standard
from .serializers import ApprovalFlowSerializer, QualityDocumentSerializer


@login_required
def preview_pdf(request, doc_id):
    """Preview the document's PDF file in the browser."""
    document = get_object_or_404(QualityDocument, id=doc_id)
    if not document.file:
        messages.error(request, "❌ The document does not have a PDF file attached.")
        return redirect("quality_docs:document_detail", doc_id=doc_id)

    return render(request, "quality_docs/document_preview.html", {"document": document})
@login_required
def download_pdf(request, doc_id):
    """Download the document's PDF file."""
    document = get_object_or_404(QualityDocument, id=doc_id)
    if not document.file:
        messages.error(request, "❌ The document does not have a PDF file attached.")
        return redirect("quality_docs:document_detail", doc_id=doc_id)

    try:
        response = FileResponse(open(document.file.path, "rb"), content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{smart_str(document.file.name)}"'
        return response
    except FileNotFoundError:
        raise Http404("PDF file not found.")

@login_required
def document_create(request):
    """Create a new document and redirect to step1 of approval setup."""
    if request.method == 'POST':
        form = QualityDocumentForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            document = form.save()

            messages.success(request, f"✅ Dokuments “{document.title}” veiksmīgi izveidots! Turpini ar saskaņošanas plūsmu.")
            return redirect("quality_docs:document_step1", doc_id=document.id)
    else:
        form = QualityDocumentForm(user=request.user)

    return render(request, 'documents/document_form.html', {'form': form})

@login_required
@permission_required("quality_docs.can_approve_documents", raise_exception=True)
def sign_and_download_pdf(request, approval_id):
    """Sign the document and allow it to be downloaded as a PDF."""
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
                    approval.approver.get_full_name(),
                )
                response = HttpResponse(open(signed_file_path, "rb"), content_type="application/pdf")
                response["Content-Disposition"] = f'attachment; filename="signed_{document.file.name}"'
                messages.success(request, f"✅ Document '{document.title}' signed and downloaded!")
                return response
            except Exception as e:
                messages.error(request, f"❌ Signing error: {e}")
        else:
            messages.error(request, "❌ Please check the entered data.")
    else:
        form = ApprovalForm()

    return render(request, "quality_docs/approve_document.html", {"form": form, "approval": approval})

def log_document_action(user, document, action):
    """Log the document action in the registry."""
    DocumentLog.objects.create(user=user, document=document, action=action)

class DocumentListView(ListView):
    """Class-based view for displaying the list of all documents."""
    model = QualityDocument
    template_name = 'quality_docs/document_list.html'
    context_object_name = 'documents'
    paginate_by = 10

    def get_queryset(self):
        """Return the list of documents."""
        return QualityDocument.objects.all()

@login_required
def document_list(request):
    """Displays the list of all documents."""
    # Legacy function-based view, consider using DocumentListView instead
    query = request.GET.get("q", "").strip()

    sections = DocumentSection.objects.prefetch_related('documents').all()

    if query:
        # filtrē dokumentus katrā sadaļā
        for section in sections:
            filtered_docs = section.documents.filter(
                Q(title__icontains=query) |
                Q(document_type__icontains=query)
            )
            section.filtered_documents = filtered_docs
    else:
        for section in sections:
            section.filtered_documents = section.documents.all()

    return render(request, "quality_docs/document_list.html", {
        "sections": sections,
        "query": query,
    })

@login_required
def document_detail(request, doc_id):
    """Displays the detailed view of the document."""
    document = get_object_or_404(QualityDocument, id=doc_id)
    return redirect("quality_docs:document_step1", doc_id=document.id)

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
    """Delete the document by its ID."""
    document = get_object_or_404(QualityDocument, id=doc_id)

    if request.method == "POST":
        document.delete()
        messages.success(request, "✅ The document was successfully deleted.")
        return redirect("quality_docs:document_list")

    return render(request, "quality_docs/document_confirm_delete.html", {"document": document})

@login_required
def document_overview(request):
    """Displays the document list."""
    # Consider using DocumentListView instead
    documents = QualityDocument.objects.all()
    return render(request, "quality_docs/document_overview.html", {"documents": documents})

# @login_required
# def akk_registrs_view(request):
#     """Displays Akk registry records."""
#     akk_records = AkkRegistrs.objects.all()
#     return render(request, "methods/templates/methods/akk_registrs.html", {"akk_records": akk_records})

@login_required
def approve_document(request, doc_id):
    """Approve the document and save the status."""
    document = get_object_or_404(QualityDocument, id=doc_id)

    if request.method == "POST":
        document.status = "approved"  # Ensure this field exists in the model
        document.save()
        messages.success(request, "✅ The document was successfully approved.")
        return redirect("quality_docs:document_detail", doc_id=document.id)

    return render(request, "quality_docs/approve_document.html", {"document": document})

class QualityDocumentViewSet(viewsets.ModelViewSet):
    """API view for the QualityDocument model"""
    queryset = QualityDocument.objects.all()
    serializer_class = QualityDocumentSerializer

class ApprovalFlowViewSet(viewsets.ModelViewSet):
    """API view for the ApprovalFlow model."""
    queryset = ApprovalFlow.objects.all()
    serializer_class = ApprovalFlowSerializer

class BasicDocumentCreateView(CreateView):
    model = QualityDocument
    form_class = BasicQualityDocumentForm
    template_name = 'quality_docs/document_upload.html'
    success_url = reverse_lazy('document_upload_success')

class StandardListView(ListView):
    model = Standard
    template_name = "quality_docs/standard_list.html"
    context_object_name = "standards"

def document_list(request):
    # Piemērs: atgriež dokumentu sarakstu
    return render(request, 'quality_docs/document_list.html')

def add_document(request):
    # Piemērs: pievieno jaunu dokumentu
    return render(request, 'quality_docs/add_document.html')

def standard_detail(request, pk):
    """Display a single standard by ID."""
    standard = get_object_or_404(Standard, pk=pk)
    return render(request, "quality_docs/standard_detail.html", {"standard": standard})

def publish_document(request, doc_id):
    """Publish the document by setting its status to 'published'."""
    document = get_object_or_404(QualityDocument, id=doc_id)
    document.status = 'published'
    document.save()
    return redirect('quality_docs:document_detail', doc_id=document.id)

def documents_for_approval(request):
    """Display a list of documents awaiting approval."""
    approvals = ApprovalFlow.objects.filter(approved=False)
    return render(request, "quality_docs/documents_for_approval.html", {"approvals": approvals})
