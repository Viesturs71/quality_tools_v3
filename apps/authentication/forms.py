from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.utils.translation import gettext_lazy as _


class CustomAuthenticationForm(AuthenticationForm):
    """
    Custom authentication form with remember me option.
    """
    remember_me = forms.BooleanField(
        required=False, 
        widget=forms.CheckboxInput(),
        label=_('Remember me'),
        help_text=_('Keep me logged in for 30 days')
    )


class CustomPasswordResetForm(PasswordResetForm):
    """
    Custom password reset form with styled email input.
    """
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'placeholder': _('Enter your email address'),
                'class': 'form-control'
            }
        ),
        label=_('Email address')
    )
