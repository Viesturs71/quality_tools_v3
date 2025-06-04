# quality_docs/forms.py
from django import forms

from .models import QualityDocument  # Pieņemot, ka šis modelis ir nepieciešams


class BasicQualityDocumentForm(forms.ModelForm):
    class Meta:
        model = QualityDocument
        fields = ["title", "document_type", "file"]

    def __init__(self, *args, **kwargs):
        kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Pievieno Bootstrap CSS klasi visiem laukiem
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

class QualityDocumentForm(forms.ModelForm):
    class Meta:
        model = QualityDocument
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Iegūst lietotāju, ja tiek padots
        super().__init__(*args, **kwargs)

        # Tikai superlietotājs drīkst mainīt sadaļu
        if user and not user.is_superuser:
            self.fields['section'].disabled = True

class ApprovalForm(forms.ModelForm):
    certificate = forms.FileField(label="Sertifikāts")
    private_key = forms.FileField(label="Privātā atslēga")
    password = forms.CharField(widget=forms.PasswordInput(), label="Parole")

    class Meta:
        model = QualityDocument
        fields = ['approval_date', 'approver']
        widgets = {
            'approval_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'approver': forms.Select(attrs={
                'class': 'form-select'
            })
        }
