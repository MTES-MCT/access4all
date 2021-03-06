# Generated by Django 3.0.3 on 2020-02-05 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0032_auto_20200205_1431'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cheminement',
            options={'verbose_name': 'Cheminement', 'verbose_name_plural': 'Cheminements'},
        ),
        migrations.AddField(
            model_name='accessibilite',
            name='aide_humaine',
            field=models.BooleanField(blank=True, help_text="Présence ou possibilité d'une aide humaine au déplacement", null=True),
        ),
        migrations.AddField(
            model_name='accessibilite',
            name='ascenseur',
            field=models.BooleanField(blank=True, help_text="Présence d'un ascenseur ou d'un élévateur", null=True, verbose_name='Ascenseur/élévateur'),
        ),
        migrations.AddField(
            model_name='accessibilite',
            name='escalier_main_courante',
            field=models.BooleanField(blank=True, help_text="Présence d'une main courante d'escalier", null=True, verbose_name='Main courante'),
        ),
        migrations.AddField(
            model_name='accessibilite',
            name='escalier_marches',
            field=models.PositiveSmallIntegerField(blank=True, help_text="Nombre de marches d'escalier. Indiquez 0 si pas d'escalier ou si présence d'un ascenseur/élévateur.", null=True, verbose_name="Marches d'escalier"),
        ),
        migrations.AddField(
            model_name='accessibilite',
            name='escalier_reperage',
            field=models.BooleanField(blank=True, help_text="Si marches contrastées, bande d'éveil ou nez de marche contrastés, indiquez “Oui”", null=True, verbose_name="Repérage de l'escalier"),
        ),
        migrations.AddField(
            model_name='accessibilite',
            name='guidage_sonore',
            field=models.BooleanField(blank=True, help_text="Présence d'un dispositif de guidage sonore", null=True, verbose_name='Système de guidage sonore'),
        ),
        migrations.AddField(
            model_name='accessibilite',
            name='largeur_mini',
            field=models.PositiveSmallIntegerField(blank=True, help_text='Largeur minimale du passage ou rétrécissement, en centimètres', null=True, verbose_name='Largeur minimale'),
        ),
        migrations.AddField(
            model_name='accessibilite',
            name='rampe',
            field=models.CharField(blank=True, choices=[(None, 'Inconnu'), ('aucune', 'Aucune'), ('fixe', 'Fixe'), ('amovible', 'Amovible')], help_text='Présence et type de rampe', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='accessibilite',
            name='reperage_vitres',
            field=models.BooleanField(blank=True, help_text="Présence d'un repérage sur les surfaces vitrées", null=True, verbose_name='Répérage surfaces vitrées'),
        ),
        migrations.AlterField(
            model_name='cheminement',
            name='type',
            field=models.CharField(choices=[('int_entree_batiment_vers_accueil', "Cheminement intérieur de l'entrée du bâtiment jusqu'à l'accueil"), ('ext_stationnement_vers_entree', "Cheminement extérieur de la place de stationnement de l'ERP à l'entrée"), ('ext_entree_parcelle_entree_vers_batiment', "Cheminement extérieur de l'entrée de la parcelle de terrain à l'entrée du bâtiment")], default='int_entree_batiment_vers_accueil', help_text='Type de circulation', max_length=100, verbose_name='Type'),
        ),
    ]
