# Generated by Django 3.0.7 on 2020-07-15 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0082_auto_20200713_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accessibilite',
            name='conformite_type',
            field=models.CharField(blank=True, choices=[(None, 'Conformité inconnue'), ('non-conforme', "L'établissement est non-conforme"), ('attestation', "L'établissement a envoyé une attestation d’accessibilité"), ('adap', "Un dossier Ad'AP a été ouvert")], max_length=255, null=True, verbose_name='Conformité'),
        ),
    ]
