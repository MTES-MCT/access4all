# Generated by Django 3.0.5 on 2020-04-22 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("erp", "0067_auto_20200420_1713"),
    ]

    operations = [
        migrations.AddField(
            model_name="accessibilite",
            name="presence_exterieur",
            field=models.BooleanField(
                blank=True,
                choices=[
                    (True, "Oui"),
                    (False, "Non"),
                    (None, "Inconnu ou sans objet"),
                ],
                help_text="L'établissement dispose-t-il d'un espace extérieur qui lui appartient ?",
                null=True,
                verbose_name="Espace extérieur",
            ),
        ),
        migrations.AlterField(
            model_name="accessibilite",
            name="transport_station_presence",
            field=models.BooleanField(
                blank=True,
                choices=[(True, "Oui"), (False, "Non"), (None, "Inconnu")],
                help_text="Présence d'une station de transport en commun à proximité (500 m)",
                null=True,
                verbose_name="Desserte par transports en commun",
            ),
        ),
    ]
