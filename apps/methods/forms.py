from django import forms
from .models import MethodInitial, MethodDetail

class MethodInitialForm(forms.ModelForm):
    class Meta:
        model = MethodInitial
        fields = '__all__'

class MethodDetailForm(forms.ModelForm):
    class Meta:
        model = MethodDetail
        fields = '__all__'
