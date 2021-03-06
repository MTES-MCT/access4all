# Generated by Django 3.0.5 on 2020-05-01 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0072_auto_20200430_2356'),
    ]

    operations = [
        migrations.RenameField(
            model_name='accessibilite',
            old_name='cheminement_terrain_accidente',
            new_name='cheminement_ext_terrain_accidente',
        ),
        migrations.AlterField(
            model_name='accessibilite',
            name='entree_balise_sonore',
            field=models.BooleanField(blank=True, choices=[(True, 'Oui'), (False, 'Non'), (None, 'Inconnu')], help_text="Présence d'une balise facilitant le repérage de la porte pour une personne aveugle ou malvoyante", null=True, verbose_name="Présence d'une balise sonore"),
        ),
        migrations.AlterField(
            model_name='accessibilite',
            name='entree_largeur_mini',
            field=models.PositiveSmallIntegerField(blank=True, help_text='Si la largeur n’est pas précisément connue, indiquez une valeur minimum. Exemple : ma largeur se situe entre 90 et 100 cm ; indiquez 90', null=True, verbose_name='Largeur minimale'),
        ),
        migrations.AlterField(
            model_name='erp',
            name='published',
            field=models.BooleanField(default=True, help_text="Statut de publication de cet ERP: si la case est décochée, l'ERP ne sera pas listé publiquement", verbose_name='Publié'),
        ),
    ]
