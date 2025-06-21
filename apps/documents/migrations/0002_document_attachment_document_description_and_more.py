from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),  # Update this to the correct previous migration
    ]

    operations = [
        # Define your migration operations here, e.g., adding fields, models, etc.
        migrations.AddField(
            model_name='document',
            name='attachment',
            field=models.FileField(
                upload_to='documents/attachments/',
                null=True,
                blank=True,
            ),
        ),
        migrations.AddField(
            model_name='document',
            name='description',
            field=models.TextField(
                null=True,
                blank=True,
            ),
        ),
        # Add other operations as needed
    ]
