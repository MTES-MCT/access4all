# Generated by Django 3.0.4 on 2020-03-12 16:36

from django.db import migrations, models
import django_better_admin_arrayfield.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ("erp", "0058_auto_20200304_2339"),
    ]

    operations = [
        migrations.RenameField(
            model_name="accessibilite",
            old_name="ascenseur",
            new_name="accueil_cheminement_ascenseur",
        ),
        migrations.RenameField(
            model_name="accessibilite",
            old_name="escalier_main_courante",
            new_name="accueil_cheminement_main_courante",
        ),
        migrations.RenameField(
            model_name="accessibilite",
            old_name="rampe",
            new_name="accueil_cheminement_rampe",
        ),
        migrations.RenameField(
            model_name="accessibilite",
            old_name="aide_humaine",
            new_name="entree_aide_humaine",
        ),
        migrations.RemoveField(
            model_name="accessibilite", name="entree_interphone",
        ),
        migrations.RemoveField(
            model_name="accessibilite", name="escalier_marches",
        ),
        migrations.RemoveField(
            model_name="accessibilite", name="escalier_reperage",
        ),
        migrations.RemoveField(
            model_name="accessibilite", name="guidage_sonore",
        ),
        migrations.RemoveField(
            model_name="accessibilite", name="largeur_mini",
        ),
        migrations.RemoveField(
            model_name="accessibilite", name="reperage_vitres",
        ),
        migrations.AddField(
            model_name="accessibilite",
            name="accueil_cheminement_nombre_marches",
            field=models.PositiveSmallIntegerField(
                blank=True,
                help_text="Indiquez 0 s’il n’y a ni marche ni escalier",
                null=True,
                verbose_name="Nombre de marches",
            ),
        ),
        migrations.AddField(
            model_name="accessibilite",
            name="accueil_cheminement_plain_pied",
            field=models.BooleanField(
                blank=True,
                choices=[
                    (True, "Oui"),
                    (False, "Non"),
                    (None, "Inconnu ou sans objet"),
                ],
                help_text="Le cheminement entre l’entrée et l’accueil est-il de plain-pied ?",
                null=True,
                verbose_name="Cheminement de plain pied",
            ),
        ),
        migrations.AddField(
            model_name="accessibilite",
            name="accueil_cheminement_reperage_marches",
            field=models.BooleanField(
                blank=True,
                choices=[(True, "Oui"), (False, "Non"), (None, "Inconnu")],
                help_text="Nez de marche contrasté, bande d'éveil à la vigilance en haut de l'escalier, première et dernière contremarches de l'escalier contrastées",
                null=True,
                verbose_name="Repérage des marches ou de l’escalier",
            ),
        ),
        migrations.AddField(
            model_name="accessibilite",
            name="accueil_retrecissement",
            field=models.BooleanField(
                blank=True,
                choices=[(True, "Oui"), (False, "Non"), (None, "Inconnu")],
                help_text="Existe-t-il un ou plusieurs rétrécissements (inférieur à 80 cm) du chemin emprunté par le public pour atteindre la zone d’accueil ?",
                null=True,
                verbose_name="Rétrécissement du cheminement",
            ),
        ),
        migrations.AddField(
            model_name="accessibilite",
            name="cheminement_ext_ascenseur",
            field=models.BooleanField(
                blank=True,
                choices=[(True, "Oui"), (False, "Non"), (None, "Inconnu")],
                help_text="Présence d'un ascenseur ou d'un élévateur",
                null=True,
                verbose_name="Ascenseur/élévateur",
            ),
        ),
        migrations.AddField(
            model_name="accessibilite",
            name="cheminement_ext_bande_guidage",
            field=models.BooleanField(
                blank=True,
                choices=[(True, "Oui"), (False, "Non"), (None, "Inconnu")],
                help_text="Présence d'une bande de guidage au sol facilitant le déplacement d'une personne aveugle ou malvoyante",
                null=True,
                verbose_name="Bande de guidage",
            ),
        ),
        migrations.AddField(
            model_name="accessibilite",
            name="cheminement_ext_devers",
            field=models.CharField(
                blank=True,
                choices=[
                    ("aucun", "Aucun"),
                    ("léger", "Léger"),
                    ("important", "Important"),
                    (None, "Inconnu ou sans objet"),
                ],
                help_text="Inclinaison transversale du cheminement",
                max_length=15,
                null=True,
                verbose_name="Dévers",
            ),
        ),
        migrations.AddField(
            model_name="accessibilite",
            name="cheminement_ext_guidage_sonore",
            field=models.BooleanField(
                blank=True,
                choices=[(True, "Oui"), (False, "Non"), (None, "Inconnu")],
                help_text="Présence d'un système de guidage sonore aidant le déplacement d'une personne aveugle ou malvoyante",
                null=True,
                verbose_name="Système de guidage sonore",
            ),
        ),
        migrations.AddField(
            model_name="accessibilite",
            name="cheminement_ext_main_courante",
            field=models.BooleanField(
                blank=True,
                choices=[
                    (True, "Oui"),
                    (False, "Non"),
                    (None, "Inconnu ou sans objet"),
                ],
                help_text="Présence d'une main courante d'escalier",
                null=True,
                verbose_name="Main courante",
            ),
        ),
        migrations.AddField(
            model_name="accessibilite",
            name="cheminement_ext_nombre_marches",
            field=models.PositiveSmallIntegerField(
                blank=True,
                help_text="Indiquez 0 s’il n’y a ni marche ni escalier",
                null=True,
                verbose_name="Nombre de marches",
            ),
        ),
        migrations.AddField(
            model_name="accessibilite",
            name="cheminement_ext_pente",
            field=models.CharField(
                blank=True,
                choices=[
                    ("aucune", "Aucune"),
                    ("légère", "Légère"),
                    ("importante", "Importante"),
                    (None, "Inconnu ou sans objet"),
                ],
                help_text="Présence et type de pente",
                max_length=15,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="accessibilite",
            name="cheminement_ext_plain_pied",
            field=models.BooleanField(
                blank=True,
                choices=[(True, "Oui"), (False, "Non"), (None, "Inconnu")],
                help_text="Le cheminement est-il de plain-pied ou existe-t-il une rupture de niveau entraînant la présence de marches ou d'un équipement type ascenseur ?",
                null=True,
                verbose_name="Cheminement de plain-pied",
            ),
        ),
        migrations.AddField(
            model_name="accessibilite",
            name="cheminement_ext_rampe",
            field=models.CharField(
                blank=True,
                choices=[
                    ("aucune", "Aucune"),
                    ("fixe", "Fixe"),
                    ("amovible", "Amovible"),
                    (None, "Inconnu"),
                ],
                help_text="Présence et type de rampe",
                max_length=20,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="accessibilite",
            name="cheminement_ext_reperage_marches",
            field=models.BooleanField(
                blank=True,
                choices=[(True, "Oui"), (False, "Non"), (None, "Inconnu")],
                help_text="Nez de marche contrasté, bande d'éveil à la vigilance en haut de l'escalier, première et dernière contremarches de l'escalier contrastées",
                null=True,
                verbose_name="Repérage des marches ou de l’escalier",
            ),
        ),
        migrations.AddField(
            model_name="accessibilite",
            name="cheminement_ext_retrecissement",
            field=models.BooleanField(
                blank=True,
                choices=[(True, "Oui"), (False, "Non"), (None, "Inconnu")],
                help_text="Existe-t-il un ou plusieurs rétrécissements (inférieur à 80 cm) du chemin emprunté par le public pour atteindre l'entrée ?",
                null=True,
                verbose_name="Rétrécissment du cheminement",
            ),
        ),
        migrations.AddField(
            model_name="accessibilite",
            name="entree_ascenseur",
            field=models.BooleanField(
                blank=True,
                choices=[(True, "Oui"), (False, "Non"), (None, "Inconnu")],
                help_text="Présence d'un ascenseur ou d'un élévateur",
                null=True,
                verbose_name="Ascenseur/élévateur",
            ),
        ),
        migrations.AddField(
            model_name="accessibilite",
            name="entree_dispositif_appel",
            field=models.BooleanField(
                blank=True,
                choices=[(True, "Oui"), (False, "Non"), (None, "Inconnu")],
                help_text="Existe-t-il un dispositif comme une sonnette pour permettre à quelqu'un ayant besoin de la rampe de signaler sa présence ?",
                null=True,
                verbose_name="Dispositif d'appel",
            ),
        ),
        migrations.AddField(
            model_name="accessibilite",
            name="entree_largeur_mini",
            field=models.PositiveSmallIntegerField(
                blank=True,
                help_text="Si la largeur n’est pas précisément connue, indiquez une valeur minimum. Exemple : ma largeur se situe entre 90 et 100 cm ; indiquez 90.",
                null=True,
                verbose_name="Largeur minimale",
            ),
        ),
        migrations.AddField(
            model_name="accessibilite",
            name="entree_marches",
            field=models.PositiveSmallIntegerField(
                blank=True,
                help_text="Nombre de marches d'escalier",
                null=True,
                verbose_name="Marches d'escalier",
            ),
        ),
        migrations.AddField(
            model_name="accessibilite",
            name="entree_marches_main_courante",
            field=models.BooleanField(
                blank=True,
                choices=[
                    (True, "Oui"),
                    (False, "Non"),
                    (None, "Inconnu ou sans objet"),
                ],
                help_text="Présence d'une main courante pour franchir les marches",
                null=True,
                verbose_name="Main courante",
            ),
        ),
        migrations.AddField(
            model_name="accessibilite",
            name="entree_marches_rampe",
            field=models.CharField(
                blank=True,
                choices=[
                    ("aucune", "Aucune"),
                    ("fixe", "Fixe"),
                    ("amovible", "Amovible"),
                    (None, "Inconnu"),
                ],
                help_text="Présence et type de rampe",
                max_length=20,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="accessibilite",
            name="entree_marches_reperage",
            field=models.BooleanField(
                blank=True,
                choices=[
                    (True, "Oui"),
                    (False, "Non"),
                    (None, "Inconnu ou sans objet"),
                ],
                help_text="Nez de marche contrasté, bande d'éveil à la vigilance en haut de l'escalier, première et dernière contremarches de l'escalier contrastées",
                null=True,
                verbose_name="Repérage de l'escalier",
            ),
        ),
        migrations.AddField(
            model_name="accessibilite",
            name="entree_reperage_vitres",
            field=models.BooleanField(
                blank=True,
                choices=[
                    (True, "Oui"),
                    (False, "Non"),
                    (None, "Inconnu ou sans objet"),
                ],
                help_text="Si l'entrée est vitrée, présence d'éléments contrastés permettant de visualiser l'entrée (vitrophanie) ?",
                null=True,
                verbose_name="Entrée vitrée",
            ),
        ),
        migrations.AddField(
            model_name="accessibilite",
            name="labels_autre",
            field=models.CharField(
                blank=True,
                help_text="Si autre, précisez le nom du label",
                max_length=255,
                null=True,
                verbose_name="Autre label",
            ),
        ),
        migrations.AddField(
            model_name="accessibilite",
            name="labels_familles_handicap",
            field=django_better_admin_arrayfield.models.fields.ArrayField(
                base_field=models.CharField(blank=True, max_length=255),
                blank=True,
                choices=[
                    ("auditif", "auditif"),
                    ("mental", "mental"),
                    ("moteur", "moteur"),
                    ("visuel", "visuel"),
                ],
                default=list,
                null=True,
                size=None,
                verbose_name="Famille(s) de handicap concernées(s)",
            ),
        ),
        migrations.AlterField(
            model_name="accessibilite",
            name="accueil_equipements_malentendants",
            field=models.ManyToManyField(
                blank=True,
                help_text="L'accueil est-il équipé de produits ou prestations dédiés aux personnes sourdes ou malentendantes (boucle à induction magnétique, langue des signes françaises, solution de traduction à distance, etc)",
                to="erp.EquipementMalentendant",
                verbose_name="Équipements sourds/malentendants",
            ),
        ),
        migrations.AlterField(
            model_name="accessibilite",
            name="accueil_personnels",
            field=models.CharField(
                blank=True,
                choices=[
                    ("aucun", "Aucun personnel"),
                    ("formés", "Personnels sensibilisés et formés"),
                    ("non-formés", "Personnels non-formés"),
                    (None, "Inconnu"),
                ],
                help_text="Présence et sensibilisation du personnel d'accueil",
                max_length=255,
                null=True,
                verbose_name="Personnel d'accueil",
            ),
        ),
        migrations.AlterField(
            model_name="accessibilite",
            name="accueil_prestations",
            field=models.TextField(
                blank=True,
                help_text="Veuillez indiquer ici les prestations spécifiques supplémentaires proposées par l'établissement",
                max_length=1000,
                null=True,
                verbose_name="Prestations d'accueil adapté supplémentaires",
            ),
        ),
        migrations.AlterField(
            model_name="accessibilite",
            name="accueil_visibilite",
            field=models.BooleanField(
                blank=True,
                choices=[(True, "Oui"), (False, "Non"), (None, "Inconnu")],
                help_text="La zone d'accueil (guichet d’accueil, caisse, secrétariat, etc) est-elle visible depuis l'entrée ?",
                null=True,
                verbose_name="Visibilité directe de la zone d'accueil depuis l'entrée",
            ),
        ),
        migrations.AlterField(
            model_name="accessibilite",
            name="entree_plain_pied",
            field=models.BooleanField(
                blank=True,
                choices=[(True, "Oui"), (False, "Non"), (None, "Inconnu")],
                help_text="L'entrée est-elle de plain-pied ?",
                null=True,
                verbose_name="Entrée de plain-pied",
            ),
        ),
        migrations.AlterField(
            model_name="accessibilite",
            name="entree_reperage",
            field=models.BooleanField(
                blank=True,
                choices=[
                    (True, "Oui"),
                    (False, "Non"),
                    (None, "Inconnu ou sans objet"),
                ],
                help_text="Y a-t-il des éléments de repérage de l'entrée (numéro de rue à proximité, enseigne, etc)",
                null=True,
                verbose_name="Entrée facilement repérable",
            ),
        ),
        migrations.AlterField(
            model_name="accessibilite",
            name="labels",
            field=models.ManyToManyField(
                blank=True,
                help_text="Labels d'accessibilité obtenus par l'ERP",
                to="erp.Label",
                verbose_name="Labels d'accessibilité",
            ),
        ),
        migrations.AlterField(
            model_name="accessibilite",
            name="stationnement_ext_pmr",
            field=models.BooleanField(
                blank=True,
                choices=[(True, "Oui"), (False, "Non"), (None, "Inconnu")],
                help_text="Existe-t-il une ou plusieurs places de stationnement en voirie ou en parking à proximité de l'ERP (200m) ?",
                null=True,
                verbose_name="Stationnements PMR à proximité de l'ERP",
            ),
        ),
        migrations.AlterField(
            model_name="accessibilite",
            name="stationnement_ext_presence",
            field=models.BooleanField(
                blank=True,
                choices=[(True, "Oui"), (False, "Non"), (None, "Inconnu")],
                help_text="Présence de stationnements à proximité de l'ERP (200m)",
                null=True,
                verbose_name="Stationnement à proximité de l'ERP",
            ),
        ),
        migrations.AlterField(
            model_name="accessibilite",
            name="stationnement_pmr",
            field=models.BooleanField(
                blank=True,
                choices=[(True, "Oui"), (False, "Non"), (None, "Inconnu")],
                help_text="Existe-t-il une ou plusieurs places de stationnement adaptées ?",
                null=True,
                verbose_name="Stationnements PMR dans l'ERP",
            ),
        ),
        migrations.AlterField(
            model_name="accessibilite",
            name="stationnement_presence",
            field=models.BooleanField(
                blank=True,
                choices=[(True, "Oui"), (False, "Non"), (None, "Inconnu")],
                help_text="Existe-t-il une ou plusieurs places de stationnement au sein de la parcelle de l'ERP ?",
                null=True,
                verbose_name="Stationnement dans l'ERP",
            ),
        ),
        migrations.DeleteModel(name="Cheminement",),
    ]