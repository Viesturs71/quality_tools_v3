from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),  # Update this to the correct previous migration
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='uploaded_by',
            field=models.ForeignKey(
                to='auth.User',
                on_delete=django.db.models.deletion.CASCADE,
                related_name='uploaded_documents',
                null=True,
                blank=True,
            ),
        ),
    ]
