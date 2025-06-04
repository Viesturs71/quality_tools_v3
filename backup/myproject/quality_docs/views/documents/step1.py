from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import UpdateView

from quality_docs.forms.step1 import DocumentStep1Form
from quality_docs.models.documents import QualityDocument


class Step1View(LoginRequiredMixin, UpdateView):
    """First step in document creation workflow - basic information setup"""
    model = QualityDocument
    form_class = DocumentStep1Form
    template_name = 'quality_docs/document_step1.html'
    pk_url_kwarg = 'doc_id'

    def get_success_url(self):
        """Redirect to the next step"""
        return reverse('quality_docs:document_detail', kwargs={'doc_id': self.object.id})

    def form_valid(self, form):
        """Update creation_step if form is valid"""
        response = super().form_valid(form)

        # Update creation step
        self.object.creation_step = 2
        self.object.save()

        messages.success(self.request, _("Basic information saved successfully."))
        return response
