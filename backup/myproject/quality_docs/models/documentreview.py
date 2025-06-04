from django.db import models
from django.utils import timezone

class DocumentReview(models.Model):
    # ...existing fields...
    created_at = models.DateTimeField(auto_now_add=True, default=timezone.now)
    # ...existing code...