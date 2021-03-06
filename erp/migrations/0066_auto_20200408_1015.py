# Generated by Django 3.0.5 on 2020-04-08 08:15

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0065_auto_20200313_1436'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accessibilite',
            name='labels_familles_handicap',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, choices=[('auditif', 'Auditif'), ('mental', 'Mental'), ('moteur', 'Moteur'), ('visuel', 'Visuel')], max_length=255), blank=True, default=list, help_text="Liste des familles de handicaps couverts par l'obtention de ce label", null=True, size=None, verbose_name='Famille(s) de handicap concernées(s)'),
        ),
        migrations.AlterField(
            model_name='erp',
            name='code_insee',
            field=models.CharField(blank=True, help_text='Code INSEE de la commune', max_length=5, null=True, verbose_name='Code INSEE'),
        ),
    ]
