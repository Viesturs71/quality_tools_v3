#quality_docs/models/approval_flow.py
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from quality_docs.models.documents import QualityDocument
from quality_docs.services.pdf_signer import sign_pdf_document

User = get_user_model()


class ApprovalFlow(models.Model):
    """Dokumentu apstiprināšanas plūsmas modelis ar parakstīšanu un noraidīšanu."""

    STATUS_CHOICES = [
        ("pending", _("Gaida")),
        ("approved", _("Apstiprināts")),
        ("rejected", _("Noraidīts")),
    ]

    document = models.ForeignKey(
        QualityDocument, on_delete=models.CASCADE, related_name="approval_flows", verbose_name=_("Dokuments")
    )
    approver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="approval_flows", verbose_name=_("Apstiprinātājs")
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending", verbose_name=_("Statuss")
    )
    signed_pdf = models.FileField(
        upload_to="signed_documents/", null=True, blank=True, verbose_name=_("Parakstītais dokuments")
    )
    rejection_reason = models.TextField(
        null=True, blank=True, verbose_name=_("Noraidīšanas iemesls")
    )
    approved_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Apstiprināšanas datums"))
    rejected_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Noraidīšanas datums"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Izveides datums"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Atjaunināšanas datums"))

# Jaunais lauks - grupu apstiprināšanai
    approval_group = models.IntegerField(
        default=1,
        verbose_name=_("Apstiprināšanas grupa"),
        help_text=_("Apstiprināšanas grupa. Lietotāji ar vienādu grupu apstiprina dokumentu paralēli.")
    )
    review_order = models.IntegerField(
        default=1,
        verbose_name=_("Secības numurs"),
        help_text=_("Norāda apstiprināšanas secību. Zemākā vērtība nozīmē, ka grupa apstiprina vispirms.")
    )

    class Meta:
        verbose_name = _("Apstiprināšanas plūsma")
        verbose_name_plural = _("Apstiprināšanas plūsmas")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.document.title} - {self.approver.get_full_name()} ({self.get_status_display()})"

    def approve(self, certificate, private_key, password):
        """Apstiprina dokumentu, paraksta PDF un saglabā statusu."""
        if self.status == "approved":
            raise ValueError("Dokuments jau ir apstiprināts.")
        if not self.document.file:
            raise ValueError("Nav pievienots dokuments parakstīšanai.")

        try:
            signed_file_path = sign_pdf_document(
                self.document.file.path,
                certificate,
                private_key,
                password,
                self.approver.get_full_name(),
            )
            with open(signed_file_path, "rb") as pdf_file:
                self.signed_pdf.save(signed_file_path, pdf_file)
            self.status = "approved"
            self.approved_at = timezone.now()
            self.save()
        except Exception as e:
            raise ValueError(f"Parakstīšanas kļūda: {e}")

    def reject(self, reason):
        """Noraida dokumentu ar norādītu iemeslu."""
        if self.status == "rejected":
            raise ValueError("Dokuments jau ir noraidīts.")
        self.status = "rejected"
        self.rejection_reason = reason
        self.rejected_at = timezone.now()
        self.save()

    def is_pending(self):
        """Pārbauda, vai apstiprināšana vēl gaida."""
        return self.status == "pending"

    def is_approved(self):
        """Pārbauda, vai dokuments ir apstiprināts."""
        return self.status == "approved"

    def is_rejected(self):
        """Pārbauda, vai dokuments ir noraidīts."""
        return self.status == "rejected"

def is_active_for_approval(self):
        """
        Pārbauda, vai šis apstiprināšanas ieraksts ir aktīvs un gaida apstiprinājumu.
        Ieraksts ir aktīvs, ja tas ir statusā "pending" un visas iepriekšējās grupas
        ir pilnībā apstiprinājušas dokumentu.
        """
        if self.status != "pending":
            return False

        # Pārbaudam, vai visas iepriekšējās grupas ir apstiprinājušas
        previous_groups = ApprovalFlow.objects.filter(
            document=self.document,
            review_order__lt=self.review_order
        ).exclude(status="approved")

        # Ja ir kāda iepriekšēja grupa, kas nav pilnībā apstiprināta, tad šī nav aktīva
        return not previous_groups.exists()


class DocumentReview(models.Model):
    """Model for tracking document reviews"""

    STATUS_CHOICES = [
        ("pending", _("Pending")),
        ("approved", _("Approved")),
        ("rejected", _("Rejected")),
    ]

    document = models.ForeignKey(
        QualityDocument,
        on_delete=models.CASCADE,
        related_name='document_reviews',  # Changed this from review_flows
        verbose_name=_("Document")
    )

    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='document_reviews',
        verbose_name=_("Reviewer")
    )

    review_order = models.PositiveIntegerField(
        _("Review Order"),
        help_text=_("Order in which this reviewer should review (for sequential review)"),
    )

    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    comments = models.TextField(
        _("Review Comments"),
        blank=True,
        null=True
    )

    reviewed_at = models.DateTimeField(
        _("Reviewed At"),
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['review_order']
        verbose_name = _("Document Review")
        verbose_name_plural = _("Document Reviews")
        unique_together = ['document', 'review_order']

    def save(self, *args, **kwargs):
        if self.status in ["approved", "rejected"] and not self.reviewed_at:
            self.reviewed_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.document} - {self.reviewer} ({self.get_status_display()})"

