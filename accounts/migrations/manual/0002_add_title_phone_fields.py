# This is a placeholder for a future migration - DO NOT RUN YET
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),  # Make sure this matches your latest migration
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='title'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='phone number'),
        ),
    ]
