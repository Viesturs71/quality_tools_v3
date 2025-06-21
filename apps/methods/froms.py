from django import forms
from .models import MetozuRegistrs

class MethodInitialForm(forms.ModelForm):
    class Meta:
        model = MetozuRegistrs
        # list only those fields you want in the “create” form:
        fields = [
            'name',
            'description',
            'created_by',
            # …add other fields as appropriate…
        ]

class MethodDetailForm(forms.ModelForm):
    class Meta:
        model = MetozuRegistrs
        # show all fields (or narrow this down if needed):
        fields = '__all__'
