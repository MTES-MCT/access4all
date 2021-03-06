# Generated by Django 3.0.3 on 2020-02-27 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0052_auto_20200227_1457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accessibilite',
            name='accueil_personnels',
            field=models.CharField(blank=True, choices=[('aucun', 'Aucun personnel'), ('formés', 'Personnels sensibilisés et formés'), ('non-formés', 'Personnels non-formés'), (None, 'Inconnu')], help_text="Présence et type de personnel d'accueil", max_length=255, null=True, verbose_name="Personnel d'accueil"),
        ),
        migrations.AlterField(
            model_name='accessibilite',
            name='rampe',
            field=models.CharField(blank=True, choices=[('aucune', 'Aucune'), ('fixe', 'Fixe'), ('amovible', 'Amovible'), (None, 'Inconnu')], help_text='Présence et type de rampe', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='cheminement',
            name='rampe',
            field=models.CharField(blank=True, choices=[('aucune', 'Aucune'), ('fixe', 'Fixe'), ('amovible', 'Amovible'), (None, 'Inconnu')], help_text='Présence et type de rampe', max_length=20, null=True),
        ),
    ]
