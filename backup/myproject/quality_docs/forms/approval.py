from django import forms
from django.utils.translation import gettext_lazy as _

from quality_docs.models.approval_flow import ApprovalFlow


class ApprovalForm(forms.ModelForm):
    certificate = forms.FileField(
        label=_("Digital Certificate"),
        required=True,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    private_key = forms.FileField(
        label=_("Private Key"),
        required=True,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    password = forms.CharField(
        label=_("Certificate Password"),
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = ApprovalFlow
        fields = ['certificate', 'private_key', 'password']
