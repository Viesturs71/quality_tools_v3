from django.db import models

class DocumentAttachment(models.Model):
    document = models.ForeignKey('Document', on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='document_attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Attachment for {self.document}"