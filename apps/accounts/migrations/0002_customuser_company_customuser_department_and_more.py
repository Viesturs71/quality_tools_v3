from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),  # Update this to the correct previous migration
    ]

    operations = [
        # Define your migration operations here, e.g., adding fields, models, etc.
        migrations.AddField(
            model_name='customuser',
            name='company',
            field=models.ForeignKey(
                to='company.Company',
                on_delete=models.CASCADE,
                null=True,
                blank=True,
            ),
        ),
        migrations.AddField(
            model_name='customuser',
            name='department',
            field=models.ForeignKey(
                to='company.Department',
                on_delete=models.CASCADE,
                null=True,
                blank=True,
            ),
        ),
        # Add other operations as needed
    ]
