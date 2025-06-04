from django import forms

from quality_docs.models.documents import QualityDocument


class QualityDocumentForm(forms.ModelForm):
    class Meta:
        model = QualityDocument
        fields = [
            'title',
            'document_type',
            'description',
            'file',
            'version',
            'document_identifier'
        ]

    def __init__(self, *args, **kwargs):
        kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
