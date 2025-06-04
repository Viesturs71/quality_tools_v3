from django import forms


class ApprovalForm(forms.Form):
    certificate = forms.FileField()
    private_key = forms.FileField()
    password = forms.CharField(widget=forms.PasswordInput)
