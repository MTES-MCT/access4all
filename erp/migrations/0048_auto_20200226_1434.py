# Generated by Django 3.0.3 on 2020-02-26 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0047_auto_20200226_1245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='erp',
            name='numero',
            field=models.CharField(blank=True, help_text='Numéro dans la voie, incluant le complément (BIS, TER, etc.)', max_length=30, null=True, verbose_name='Numéro'),
        ),
    ]
