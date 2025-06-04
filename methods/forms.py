#methods/forms.py
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Submit
from django import forms

from .models import MetozuRegistrs


class MethodInitialForm(forms.ModelForm):
    class Meta:
        model = MetozuRegistrs
        fields = ['name', 'identification']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('name'),
            Field('identification'),
            Submit('submit', 'Izveidot metodi', css_class='btn btn-primary mt-3')
        )

class MethodDetailForm(forms.ModelForm):
    class Meta:
        model = MetozuRegistrs
        fields = ['investigation_field', 'analyzer', 'technology',
                 'test_material', 'document']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            Field('investigation_field'),
            Field('analyzer'),
            Field('technology'),
            Field('test_material'),
            Field('document'),
            Submit('submit', 'Saglabāt izmaiņas', css_class='btn btn-primary mt-3')
        )
