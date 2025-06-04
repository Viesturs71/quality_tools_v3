# quality_docs/forms/step1.py

from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from quality_docs.models.documents import QualityDocument

User = get_user_model()

class DocumentStep1Form(forms.ModelForm):
    """First step form - document basic info and approval workflow"""
    reviewers = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(is_active=True),
        required=True,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control select2',
            'data-placeholder': _('Select reviewers')
        }),
        help_text=_('Select users who need to review this document')
    )

    review_type = forms.ChoiceField(
        choices=QualityDocument.REVIEW_TYPE_CHOICES,
        widget=forms.RadioSelect,
        initial='sequential',
        help_text=_('Choose how reviewers should process the document')
    )

    comments = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': _('Add your comments about the document')
        }),
        required=False
    )

    class Meta:
        model = QualityDocument
        fields = ['reviewers', 'review_type', 'comments']

    def save(self, commit=True):
        document = super().save(commit=False)
        if commit:
            document.save()
            self.save_reviewers(document)
        return document

    def save_reviewers(self, document):
        """Save reviewers with proper ordering"""
        document.reviewers.clear()
        reviewers = self.cleaned_data['reviewers']
        for index, reviewer in enumerate(reviewers, 1):
            document.document_reviews.create(
                reviewer=reviewer,
                review_order=index,
                status='pending'
            )
