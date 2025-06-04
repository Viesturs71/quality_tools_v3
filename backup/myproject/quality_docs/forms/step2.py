# quality_docs/forms/step2.py
from django import forms
from django.utils.translation import gettext_lazy as _

from quality_docs.models import QualityDocument


class DocumentStep2Form(forms.ModelForm):
    """Second step form - document details"""
    class Meta:
        model = QualityDocument
        fields = ['version', 'description', 'document_identifier']
        widgets = {
            'version': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Enter document version')
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': _('Enter document description')
            }),
            'document_identifier': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Enter document identifier')
            })
        }
