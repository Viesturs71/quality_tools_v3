# Generated by Django 4.2.20 on 2025-06-29 15:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("company", "0001_initial"),
        ("personnel", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="department",
            name="head",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="headed_departments",
                to="personnel.employee",
                verbose_name="Department Head",
            ),
        ),
        migrations.AddField(
            model_name="department",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="subdepartments",
                to="company.department",
                verbose_name="Parent Department",
            ),
        ),
    ]
