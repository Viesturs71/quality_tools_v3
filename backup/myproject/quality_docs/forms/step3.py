from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from quality_docs.models import QualityDocument

User = get_user_model()

class DocumentStep3Form(forms.ModelForm):
    """Form for setting up document review workflow"""

    reviewers = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(is_active=True),
        required=True,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        help_text=_('Select users who should review this document')
    )

    review_type = forms.ChoiceField(
        choices=QualityDocument.REVIEW_TYPE_CHOICES,
        widget=forms.RadioSelect,
        initial='sequential',
        help_text=_('Choose review process type')
    )

    class Meta:
        model = QualityDocument
        fields = ['review_type']

    def save(self, commit=True):
        document = super().save(commit=False)
        if commit:
            document.save()
            # Clear existing reviewers and add new ones
            document.reviewers.clear()
            for reviewer in self.cleaned_data['reviewers']:
                document.documentreview_set.create(
                    reviewer=reviewer,
                    review_order=list(self.cleaned_data['reviewers']).index(reviewer) + 1
                )
        return document
