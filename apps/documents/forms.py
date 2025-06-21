from django import forms
from .models.document import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title']  # pielāgo pēc sava modeļa laukiem
