from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class ApprovalFlowSetupForm(forms.Form):
    """
    Form for quality managers to set up document approval workflow
    """
    reviewers = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(is_active=True),
        required=True,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control select2',
            'data-placeholder': _('Select reviewers/approvers')
        }),
        help_text=_('Select users who will review and approve this document')
    )

    review_type = forms.ChoiceField(
        choices=[
            ('sequential', _('Sequential (One by one)')),
            ('parallel', _('Parallel (All at once)')),
            ('combined', _('Combined (Groups)')), # Pievienojam jaunu izvēli
        ],
        widget=forms.RadioSelect,
        initial='sequential',
        help_text=_('Choose approval flow type')
    )

    # Lauki dinamiskajām grupām
    approval_groups = forms.JSONField(required=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        self.document = kwargs.pop('document', None)
        super().__init__(*args, **kwargs)

        # Ņemam vērā tikai aktīvus lietotājus ar noteiktām atļaujām
        self.fields['reviewers'].queryset = User.objects.filter(
            is_active=True
        ).order_by('first_name', 'last_name')
