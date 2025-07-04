# Generated by Django 4.2.20 on 2025-06-26 12:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Document",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="Title")),
                (
                    "document_number",
                    models.CharField(
                        max_length=50, unique=True, verbose_name="Document Number"
                    ),
                ),
                (
                    "version",
                    models.CharField(
                        default="1.0", max_length=20, verbose_name="Version"
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="Description"),
                ),
                ("content", models.TextField(blank=True, verbose_name="Content")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("draft", "Draft"),
                            ("review", "In Review"),
                            ("approved", "Approved"),
                            ("published", "Published"),
                            ("archived", "Archived"),
                        ],
                        default="draft",
                        max_length=20,
                        verbose_name="Status",
                    ),
                ),
                (
                    "document_type",
                    models.CharField(
                        choices=[
                            ("procedure", "Procedure"),
                            ("instruction", "Work Instruction"),
                            ("form", "Form"),
                            ("template", "Template"),
                            ("record", "Record"),
                            ("report", "Report"),
                            ("policy", "Policy"),
                        ],
                        default="procedure",
                        max_length=20,
                        verbose_name="Document Type",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created At"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Updated At"),
                ),
                (
                    "approved_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Approved At"
                    ),
                ),
                (
                    "published_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Published At"
                    ),
                ),
                (
                    "approved_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="approved_documents",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Approved By",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="created_documents",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created By",
                    ),
                ),
                (
                    "parent_document",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="child_documents",
                        to="documents.document",
                        verbose_name="Parent Document",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="updated_documents",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Updated By",
                    ),
                ),
            ],
            options={
                "verbose_name": "Document",
                "verbose_name_plural": "Documents",
                "ordering": ["-updated_at"],
            },
        ),
        migrations.CreateModel(
            name="DocumentSection",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="Title")),
                ("content", models.TextField(blank=True, verbose_name="Content")),
                ("order", models.PositiveIntegerField(default=0, verbose_name="Order")),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created At"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Updated At"),
                ),
                (
                    "document",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sections",
                        to="documents.document",
                        verbose_name="Document",
                    ),
                ),
            ],
            options={
                "verbose_name": "Document Section",
                "verbose_name_plural": "Document Sections",
                "ordering": ["document", "order"],
            },
        ),
        migrations.CreateModel(
            name="DocumentRevision",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "revision_number",
                    models.CharField(max_length=20, verbose_name="Revision Number"),
                ),
                ("revision_date", models.DateField(verbose_name="Revision Date")),
                ("description", models.TextField(verbose_name="Description")),
                (
                    "is_current",
                    models.BooleanField(default=False, verbose_name="Current Revision"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created At"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Updated At"),
                ),
                (
                    "document",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="documents.document",
                    ),
                ),
            ],
            options={
                "verbose_name": "Document Revision",
                "verbose_name_plural": "Document Revisions",
                "ordering": ["-revision_date"],
            },
        ),
        migrations.CreateModel(
            name="Attachment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "file",
                    models.FileField(
                        upload_to="documents/attachments/", verbose_name="File"
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="Description"
                    ),
                ),
                (
                    "uploaded_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Uploaded At"),
                ),
                (
                    "document",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="attachments",
                        to="documents.document",
                        verbose_name="Document",
                    ),
                ),
            ],
            options={
                "verbose_name": "Attachment",
                "verbose_name_plural": "Attachments",
                "ordering": ["-uploaded_at"],
            },
        ),
        migrations.CreateModel(
            name="SectionDocumentLink",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="Link Description"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created At"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Updated At"),
                ),
                (
                    "document",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="section_links",
                        to="documents.document",
                        verbose_name="Document",
                    ),
                ),
                (
                    "section",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="document_links",
                        to="documents.documentsection",
                        verbose_name="Section",
                    ),
                ),
            ],
            options={
                "verbose_name": "Section Document Link",
                "verbose_name_plural": "Section Document Links",
                "ordering": ("section", "document"),
                "unique_together": {("section", "document")},
            },
        ),
    ]
