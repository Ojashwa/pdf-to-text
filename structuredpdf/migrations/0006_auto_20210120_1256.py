# Generated by Django 3.1.2 on 2021-01-20 07:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('structuredpdf', '0005_auto_20210119_2133'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userpdfdata',
            old_name='invoce_date',
            new_name='invoice_date',
        ),
    ]
