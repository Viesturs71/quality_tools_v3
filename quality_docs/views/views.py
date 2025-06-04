from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, FileResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from quality_docs.models.document import (
    QualityDocument, ApprovalFlow, ApprovalStep, DocumentReview, SignatureRequest, DocumentDistribution
)
from quality_docs.forms import (
     QualityDocumentForm,
    ApprovalFlowForm,
    ApprovalStepForm,
    DocumentReviewForm,
    SignatureRequestForm,
    DocumentDistributionForm,
    DocumentApprovalForm,
    DocumentSignatureForm,
    DocumentPublishForm,
)

# ------------------ Base Views ------------------
def home(request):
    """Home view for the document management system."""
    return render(request, 'quality_docs/home.html')

# ------------------ Document Management Views ------------------
def document_list(request):
    """View to list all documents."""
    documents = QualityDocument.objects.all()
    return render(request, 'quality_docs/document_list.html', {'documents': documents})

def document_detail(request, pk):
    """View to display a single document."""
    document = get_object_or_404(QualityDocument, pk=pk)
    return render(request, 'quality_docs/document_detail.html', {'document': document})

def document_create(request):
    """View to create a new document."""
    if request.method == 'POST':
        form = QualityDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('document_list')
    else:
        form = QualityDocumentForm()
    return render(request, 'quality_docs/document_form.html', {'form': form})

def document_update(request, pk):
    """View to update an existing document."""
    document = get_object_or_404(QualityDocument, pk=pk)
    if request.method == 'POST':
        form = QualityDocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            return redirect('document_detail', pk=document.pk)
    else:
        form = QualityDocumentForm(instance=document)
    return render(request, 'quality_docs/document_form.html', {'form': form})

def document_delete(request, pk):
    """View to delete a document."""
    document = get_object_or_404(QualityDocument, pk=pk)
    document.delete()
    return redirect('document_list')

# ------------------ Workflow Views ------------------
def approval_flow_create(request, document_id):
    """View to create an approval flow for a document."""
    document = get_object_or_404(QualityDocument, pk=document_id)
    if request.method == 'POST':
        form = ApprovalFlowForm(request.POST)
        if form.is_valid():
            approval_flow = form.save(commit=False)
            approval_flow.document = document
            approval_flow.save()
            return redirect('document_detail', pk=document.pk)
    else:
        form = ApprovalFlowForm()
    return render(request, 'quality_docs/approval_flow_form.html', {'form': form})

def approval_step_create(request, flow_id):
    """View to create an approval step."""
    approval_flow = get_object_or_404(ApprovalFlow, pk=flow_id)
    if request.method == 'POST':
        form = ApprovalStepForm(request.POST)
        if form.is_valid():
            approval_step = form.save(commit=False)
            approval_step.approval_flow = approval_flow
            approval_step.save()
            return redirect('approval_flow_detail', pk=approval_flow.pk)
    else:
        form = ApprovalStepForm()
    return render(request, 'quality_docs/approval_step_form.html', {'form': form})

# ------------------ Review Views ------------------
def document_review_create(request, document_id):
    """View to create a document review."""
    document = get_object_or_404(QualityDocument, pk=document_id)
    if request.method == 'POST':
        form = DocumentReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.document = document
            review.save()
            return redirect('document_detail', pk=document.pk)
    else:
        form = DocumentReviewForm()
    return render(request, 'quality_docs/document_review_form.html', {'form': form})

# ------------------ Signature Views ------------------
def signature_request_create(request, step_id):
    """View to create a signature request."""
    approval_step = get_object_or_404(ApprovalStep, pk=step_id)
    if request.method == 'POST':
        form = SignatureRequestForm(request.POST)
        if form.is_valid():
            signature_request = form.save(commit=False)
            signature_request.approval_step = approval_step
            signature_request.save()
            return redirect('approval_step_detail', pk=approval_step.pk)
    else:
        form = SignatureRequestForm()
    return render(request, 'quality_docs/signature_request_form.html', {'form': form})

# ------------------ Distribution Views ------------------
def document_distribution_create(request, document_id):
    """View to create a document distribution."""
    document = get_object_or_404(QualityDocument, pk=document_id)
    if request.method == 'POST':
        form = DocumentDistributionForm(request.POST)
        if form.is_valid():
            distribution = form.save(commit=False)
            distribution.document = document
            distribution.save()
            return redirect('document_detail', pk=document.pk)
    else:
        form = DocumentDistributionForm()
    return render(request, 'quality_docs/document_distribution_form.html', {'form': form})

# ------------------ Approval and Signature Views ------------------
@login_required
def document_approve(request, pk):
    """
    View to handle document approval.
    This sets the is_approved flag on the document and records approval details.
    """
    document = get_object_or_404(QualityDocument, pk=pk)
    
    if request.method == 'POST':
        document.is_approved = True
        document.approval_date = timezone.now()
        document.approved_by = request.user
        document.status = 'APPROVED'
        document.save()
        
        messages.success(request, f"Document '{document.title}' has been approved.")
        return redirect('quality_docs:document_detail', pk=document.pk)
    
    return render(request, 'quality_docs/document_approve.html', {
        'document': document,
    })

@login_required
def document_sign(request, pk):
    """
    View function for signing a document electronically.
    
    This function handles the document signing process, which includes:
    1. Verifying the user has permission to sign
    2. Recording the electronic signature with timestamp
    3. Updating any related signature requests
    4. Redirecting with success message
    """
    document = get_object_or_404(QualityDocument, pk=pk)
    
    # Check the user has permission to sign this document
    if not request.user.has_perm('quality_docs.sign_documents'):
        messages.error(request, "You don't have permission to sign documents.")
        return redirect('quality_docs:document_detail', pk=document.pk)
    
    if request.method == 'POST':
        form = DocumentSignatureForm(request.POST)
        if form.is_valid():
            # Update document with signature information
            document.electronic_signature = True
            document.signature_date = timezone.now()
            document.save()
            
            # Update any pending signature requests for this user and document
            signature_requests = SignatureRequest.objects.filter(
                document=document,
                signer=request.user,
                status='PENDING'
            )
            
            for signature_request in signature_requests:
                signature_request.status = 'COMPLETED'
                signature_request.completed_date = timezone.now()
                signature_request.save()
            
            messages.success(request, f"Document '{document.title}' has been electronically signed.")
            return redirect('quality_docs:document_detail', pk=document.pk)
    else:
        form = DocumentSignatureForm()
    
    context = {
        'document': document,
        'form': form,
    }
    return render(request, 'quality_docs/document_sign.html', context)

@login_required
def document_publish(request, pk):
    """Publish an approved document."""
    document = get_object_or_404(QualityDocument, pk=pk)

    if request.method == 'POST':
        form = DocumentPublishForm(request.POST)
        if form.is_valid():
            form.publish(document, request.user)
            messages.success(request, f"Document '{document.title}' has been published.")
            return redirect('quality_docs:document_detail', pk=document.pk)
    else:
        form = DocumentPublishForm()

    return render(
        request,
        'quality_docs/document_publish.html',
        {
            'document': document,
            'form': form,
        },
    )


@login_required
def document_download(request, pk):
    """
    View for downloading document files.
    Records the download action for audit purposes.
    """
    document = get_object_or_404(QualityDocument, pk=pk)
    
    # Check if user has permission to download the document
    if not request.user.has_perm('quality_docs.view_qualitydocument') and not document.is_approved:
        raise Http404("Document not found or you don't have permission to download it.")
    
    # Record download action
    DocumentDistribution.objects.create(
        document=document,
        user=request.user,
        action_type='DOWNLOAD',
        notes=f"Downloaded by {request.user.username} at {timezone.now()}"
    )
    
    # Open the file for reading in binary mode
    try:
        file_path = document.file.path
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{document.file.name.split("/")[-1]}"'
        return response
    except Exception as e:
        # Log the error and return 404
        print(f"Error downloading file: {e}")
        raise Http404("The requested file does not exist or cannot be downloaded.")
