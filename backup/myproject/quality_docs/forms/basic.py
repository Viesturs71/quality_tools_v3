from django import forms
from django.utils.translation import gettext_lazy as _

from quality_docs.models import DocumentType, QualityDocument


class BasicQualityDocumentForm(forms.ModelForm):
    title = forms.CharField(
        label=_("Document Title"),
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _("Enter document title")
        })
    )

    document_type = forms.ModelChoiceField(
        label=_("Document Type"),
        queryset=DocumentType.objects.all(),
        required=True,
        empty_label=_("Select document type"),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    file = forms.FileField(
        label=_("Document File"),
        required=True,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        help_text=_("Upload document file")
    )

    class Meta:
        model = QualityDocument
        fields = ["title", "document_type", "file"]

    def __init__(self, *args, **kwargs):
        kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Add Bootstrap CSS class to all fields
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})
