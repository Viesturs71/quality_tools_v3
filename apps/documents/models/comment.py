from django.db import models
from django.contrib.auth.models import User


class DocumentComment(models.Model):
    """Model representing comments on quality documents."""
    document = models.ForeignKey('QualityDocument', on_delete=models.CASCADE, related_name='comments', verbose_name='Dokuments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Autors')
    text = models.TextField(verbose_name='Komentārs')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Izveidošanas datums')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atjaunināšanas datums')
    
    class Meta:
        verbose_name = 'Dokumenta komentārs'
        verbose_name_plural = 'Dokumenta komentāri'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Komentārs no {self.author.username} par {self.document.document_number}"
