from django import forms

from quality_docs.models import QualityDocument


class DocumentDetailsForm(forms.ModelForm):
    class Meta:
        model = QualityDocument
        fields = ['version', 'description', 'document_identifier']
