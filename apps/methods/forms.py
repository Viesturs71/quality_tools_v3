from django import forms
from django.utils.translation import gettext_lazy as _
from .models import (
    Method, 
    MethodInitial, 
    MethodDetail, 
    InternalQualityControl,
    ExternalQualityControl,
    MethodVerification
)

class MethodForm(forms.ModelForm):
    """
    Form for Method model with all fields.
    """
    class Meta:
        model = Method
        fields = [
            'name', 
            'identification', 
            'investigation_field', 
            'analyzer', 
            'technology',
            'test_material',
            'verification_date',
            'location',
            'document',
            'internal_qc_required',
            'external_qc_required',
            'verification_required'
        ]
        widgets = {
            'verification_date': forms.DateInput(attrs={'type': 'date'}),
            'technology': forms.Textarea(attrs={'rows': 4}),
        }


class MethodInitialForm(forms.ModelForm):
    """
    Initial form for creating a basic method.
    """
    class Meta:
        model = MethodInitial
        fields = ['name', 'description']


class MethodDetailForm(forms.ModelForm):
    """
    Detailed form for adding information to an existing method.
    """
    class Meta:
        model = MethodDetail
        fields = ['method', 'details']


class InternalQualityControlForm(forms.ModelForm):
    """
    Form for internal quality control records.
    """
    class Meta:
        model = InternalQualityControl
        fields = [
            'method',
            'control_date',
            'control_material',
            'control_lot',
            'result',
            'expected_value',
            'acceptable_range',
            'is_conforming',
            'performed_by',
            'notes'
        ]
        widgets = {
            'control_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class MethodVerificationForm(forms.ModelForm):
    """
    Form for method verification records.
    """
    class Meta:
        model = MethodVerification
        fields = [
            'method',
            'verification_type',
            'verification_date',
            'performed_by',
            'precision_data',
            'accuracy_data',
            'linearity_data',
            'detection_limit',
            'quantitation_limit',
            'acceptance_criteria',
            'results_summary',
            'protocol_document',
            'report_document'
        ]
        widgets = {
            'verification_date': forms.DateInput(attrs={'type': 'date'}),
            'precision_data': forms.Textarea(attrs={'rows': 3}),
            'accuracy_data': forms.Textarea(attrs={'rows': 3}),
            'linearity_data': forms.Textarea(attrs={'rows': 3}),
            'acceptance_criteria': forms.Textarea(attrs={'rows': 3}),
            'results_summary': forms.Textarea(attrs={'rows': 3}),
        }
