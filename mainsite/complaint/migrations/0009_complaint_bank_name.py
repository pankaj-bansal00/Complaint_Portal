# Generated by Django 5.1.6 on 2025-02-25 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complaint', '0008_remove_complaint_bank_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='bank_name',
            field=models.CharField(choices=[('hdfc', 'HDFC Bank'), ('sbi', 'State Bank of India'), ('icici', 'ICICI Bank'), ('axis', 'Axis Bank'), ('pnb', 'Punjab National Bank')], default='', max_length=50),
        ),
    ]
