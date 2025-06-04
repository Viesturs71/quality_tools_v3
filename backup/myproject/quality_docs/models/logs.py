#quality_docs/models/DocumentLog.py
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

from .documents import QualityDocument

User = get_user_model()

class DocumentLog(models.Model):
    document = models.ForeignKey(
        QualityDocument,
        on_delete=models.CASCADE,
        verbose_name="Dokuments"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Lietotājs"
    )
    action = models.CharField(
        max_length=10,
        choices=[
            ("preview", "Priekšskatījums"),
            ("download", "Lejupielāde"),
        ],
        verbose_name="Darbība"
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Laiks"
    )

    class Meta:
        verbose_name = "Dokumenta darbību žurnāls"
        verbose_name_plural = "Dokumentu darbību žurnāli"
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.document} - {self.action} by {self.user} at {self.timestamp}"
