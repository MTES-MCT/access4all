# Generated by Django 3.0.4 on 2020-03-12 18:03

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0060_auto_20200312_1859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accessibilite',
            name='labels_familles_handicap',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, choices=[('auditif', 'Auditif'), ('mental', 'Mental'), ('moteur', 'Moteur'), ('visuel', 'Visuel')], max_length=255), blank=True, default=list, null=True, size=None, verbose_name='Famille(s) de handicap concernées(s)'),
        ),
        migrations.AlterField(
            model_name='activite',
            name='mots_cles',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=40), blank=True, default=list, help_text='Liste de mots-clés apparentés à cette activité', null=True, size=None, verbose_name='Mots-clés'),
        ),
    ]
