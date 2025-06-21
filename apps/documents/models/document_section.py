from django.db import models
from .document import Document  # ...new import...

class DocumentSection(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='sections')  # Added ForeignKey to Document
    name = models.CharField(max_length=255)
    identifier = models.CharField(max_length=20)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.identifier} - {self.name}"