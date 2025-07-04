# Generated by Django 4.2.20 on 2025-06-26 15:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        (
            "documents",
            "0002_alter_documentsection_options_documentsection_code_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="documentsection",
            name="document",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sections",
                to="documents.document",
                verbose_name="Document",
            ),
        ),
    ]
