from django.db import models


class CustomPermission(models.Model):
    """
    Custom permission model for fine-grained access control.
    """
    name = models.CharField(max_length=100)
    codename = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Atļauja'
        verbose_name_plural = 'Atļaujas'
        ordering = ['name']
    
    def __str__(self):
        return self.name
