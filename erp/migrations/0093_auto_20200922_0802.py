# Generated by Django 3.1.1 on 2020-09-22 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0092_merge_20200916_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accessibilite',
            name='cheminement_ext_reperage_marches',
            field=models.BooleanField(blank=True, choices=[(True, 'Oui'), (False, 'Non'), (None, 'Inconnu ou sans objet')], null=True, verbose_name='Repérage des marches ou de l’escalier'),
        ),
    ]
