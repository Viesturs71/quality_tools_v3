"""
Quality Document model definition.
"""

from django.db import models
from django.contrib.auth.models import User

class QualityDocument(models.Model):
    # ...existing fields...
    owner = models.ForeignKey(User, default=1, on_delete=models.CASCADE, related_name="quality_documents")
    # ...existing methods...