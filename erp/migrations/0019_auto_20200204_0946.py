# Generated by Django 3.0.3 on 2020-02-04 08:46

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0018_auto_20200204_0917'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='accessibilite',
            options={'verbose_name': 'Accessibilité', 'verbose_name_plural': 'Accessibilité'},
        ),
        migrations.AlterField(
            model_name='erp',
            name='geom',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, help_text="Géolocalisation (carte rafraîchie une fois l'enregistrement sauvegardé)", null=True, srid=4326, verbose_name='Localisation'),
        ),
    ]
