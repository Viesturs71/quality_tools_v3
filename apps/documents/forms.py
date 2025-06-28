from django import forms
from django.utils.translation import gettext_lazy as _

from apps.documents.models import Document, DocumentSection, Attachment

class DocumentForm(forms.ModelForm):
    """Form for creating and editing documents."""
    
    class Meta:
        model = Document
        fields = [
            'title', 'document_number', 'version', 'status',
            'description', 'content'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'content': forms.Textarea(attrs={'class': 'rich-text-editor'}),
        }

    def clean_document_number(self):
        """Validate document number format."""
        document_number = self.cleaned_data.get('document_number')
        if document_number and not document_number.startswith('DOC-'):
            raise forms.ValidationError(_('Document number should start with DOC-'))
        return document_number
    
    def clean(self):
        """Custom validation for the entire form."""
        cleaned_data = super().clean()
        effective_date = cleaned_data.get('effective_date')
        review_date = cleaned_data.get('review_date')
        expiry_date = cleaned_data.get('expiry_date')
        
        if effective_date and expiry_date and effective_date > expiry_date:
            self.add_error('expiry_date', _('Expiry date cannot be earlier than effective date'))
        
        if effective_date and review_date and effective_date > review_date:
            self.add_error('review_date', _('Review date cannot be earlier than effective date'))
        
        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        """Initialize the form with user data if provided."""
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        """Override save to track the user who updated the document."""
        instance = super().save(commit=False)
        
        if self.user:
            if not instance.pk:  # New instance
                instance.created_by = self.user
            instance.updated_by = self.user
            
        if commit:
            instance.save()
            self.save_m2m()
            
        return instance


class DocumentSectionForm(forms.ModelForm):
    class Meta:
        model = DocumentSection
        fields = [
            'title_original', 'title_alt',
            'content_original', 'content_alt',
            'order'
        ]
        widgets = {
            'content_original': forms.Textarea(attrs={'class': 'rich-text-editor', 'rows': 5}),
            'content_alt': forms.Textarea(attrs={'class': 'rich-text-editor', 'rows': 5}),
        }


class AttachmentForm(forms.ModelForm):
    """Form for uploading document attachments."""
    
    class Meta:
        model = Attachment
        fields = ['file', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class DocumentSearchForm(forms.Form):
    """Form for searching documents."""
    
    search = forms.CharField(
        label=_('Search'),
        required=False,
        widget=forms.TextInput(attrs={'placeholder': _('Search documents...')})
    )
    status = forms.ChoiceField(
        label=_('Status'),
        required=False,
        choices=[('', _('All Statuses'))] + list(Document.STATUS_CHOICES)
    )
    date_from = forms.DateField(
        label=_('From Date'),
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    date_to = forms.DateField(
        label=_('To Date'),
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )


class DocumentVersionForm(forms.Form):
    """Form for creating a new document version."""
    
    version_notes = forms.CharField(
        label=_("Version notes"),
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text=_("Describe the changes made in this version")
    )
    
    major_version = forms.BooleanField(
        label=_("Increment major version"),
        required=False,
        help_text=_("Check to increment the major version number (e.g., 1.0 to 2.0)")
    )


class DocumentApprovalForm(forms.Form):
    """Form for approving a document."""
    
    comments = forms.CharField(
        label=_("Approval comments"),
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        help_text=_("Optional comments about the approval")
    )


class DocumentRejectionForm(forms.Form):
    """Form for rejecting a document."""
    
    reason = forms.CharField(
        label=_("Rejection reason"),
        widget=forms.Textarea(attrs={'rows': 3}),
        required=True,
        help_text=_("Provide a reason for the rejection")
    )


class DocumentFilterForm(forms.Form):
    """Form for filtering document lists."""
    
    status = forms.ChoiceField(
        label=_('Status'),
        required=False,
        choices=[('', _('All Statuses'))] + list(Document.STATUS_CHOICES)
    )
    
    author = forms.ChoiceField(
        label=_('Author'),
        required=False,
        choices=[]  # Will be populated in __init__
    )
    
    category = forms.ChoiceField(
        label=_('Category'),
        required=False,
        choices=[]  # Will be populated in __init__
    )
    
    date_from = forms.DateField(
        label=_('Created from'),
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    date_to = forms.DateField(
        label=_('Created to'),
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    def __init__(self, *args, **kwargs):
        user_choices = kwargs.pop('user_choices', [])
        category_choices = kwargs.pop('category_choices', [])
        super().__init__(*args, **kwargs)
        
        self.fields['author'].choices = [('', _('All Authors'))] + user_choices
        self.fields['category'].choices = [('', _('All Categories'))] + category_choices


class DocumentShareForm(forms.Form):
    """Form for sharing a document with users."""
    
    users = forms.MultipleChoiceField(
        label=_('Share with users'),
        required=True,
        widget=forms.SelectMultiple(attrs={'class': 'select2'}),
        choices=[]  # Will be populated in __init__
    )
    
    permission_level = forms.ChoiceField(
        label=_('Permission level'),
        required=True,
        choices=[
            ('view', _('View only')),
            ('edit', _('View and edit')),
            ('comment', _('View and comment'))
        ]
    )
    
    notify_users = forms.BooleanField(
        label=_('Send notification email'),
        required=False,
        initial=True
    )
    
    def __init__(self, *args, **kwargs):
        user_choices = kwargs.pop('user_choices', [])
        super().__init__(*args, **kwargs)
        self.fields['users'].choices = user_choices


class DocumentImportForm(forms.Form):
    """Form for importing documents from external sources."""
    
    file = forms.FileField(
        label=_('Document file'),
        required=True,
        help_text=_('Upload a file to import (PDF, DOCX, TXT)')
    )
    
    title = forms.CharField(
        label=_('Document title'),
        required=True,
        max_length=255,
        help_text=_('Enter a title for the imported document')
    )
    
    extract_text = forms.BooleanField(
        label=_('Extract text from document'),
        required=False,
        initial=True,
        help_text=_('Attempt to extract text content from the document')
    )
    
    document_category = forms.ChoiceField(
        label=_('Document category'),
        required=False,
        choices=[]  # Will be populated in __init__
    )
    
    def __init__(self, *args, **kwargs):
        category_choices = kwargs.pop('category_choices', [])
        super().__init__(*args, **kwargs)
        self.fields['document_category'].choices = [('', _('-- Select Category --'))] + category_choices
    def __init__(self, *args, **kwargs):
        category_choices = kwargs.pop('category_choices', [])
        super().__init__(*args, **kwargs)
        self.fields['document_category'].choices = [('', _('-- Select Category --'))] + category_choices
